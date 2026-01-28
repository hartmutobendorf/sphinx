
from tree_sitter import Language, Parser
try:
    import tree_sitter_d2
    HAS_D2_PARSER = True
except ImportError:
    HAS_D2_PARSER = False

def merge_d2_content(diagram_code, config_code):
    if not HAS_D2_PARSER:
        return config_code + "\n" + diagram_code

    D2_LANGUAGE = Language(tree_sitter_d2.language())
    parser = Parser(D2_LANGUAGE)
    
    config_tree = parser.parse(bytes(config_code, "utf8"))
    diagram_tree = parser.parse(bytes(diagram_code, "utf8"))
    
    # Helper: get key from declaration node
    def get_key(node, source_code):
        # Scan children for identifier or string acting as key
        # In D2, the structure is commonly identifier + colon
        # But looking at children types is safest
        for child in node.children:
            if child.type in ('identifier', 'string', 'keyword'):
                return source_code[child.start_byte:child.end_byte]
        return None

    # Helper: find a top-level key in a block node (not including nested)
    def find_key_in_block(block_node, search_key, source_code):
        for child in block_node.children:
            if child.type == 'declaration':
                k = get_key(child, source_code)
                if k == search_key:
                    return child
        return None

    # Helper: extract text including trailing inline comment
    def get_text_with_comment(node, source_code, block_node):
        # check next sibling
        # We need to find the node in child list to get next sibling reliably?
        # tree-sitter nodes have next_sibling property
        end_byte = node.end_byte
        nxt = node.next_sibling
        if nxt and nxt.type == 'comment':
            # check if on same line?
            # actually we can just grab it if it's there
            end_byte = nxt.end_byte
        
        return source_code[node.start_byte:end_byte]

    # 1. Locate 'vars' in both
    config_vars_decl = None
    # We search the root
    for child in config_tree.root_node.children:
        if child.type == 'declaration':
            if get_key(child, config_code) == 'vars':
                config_vars_decl = child
                break
    
    if not config_vars_decl:
        return diagram_code # Nothing to merge from config
        
    diagram_vars_decl = None
    for child in diagram_tree.root_node.children:
        if child.type == 'declaration':
            if get_key(child, diagram_code) == 'vars':
                diagram_vars_decl = child
                break
    
    # If diagram has no vars, prepend config vars block
    if not diagram_vars_decl:
        return config_code.strip() + "\n\n" + diagram_code

    # 2. Inside vars, locate d2-config
    # We need the BLOCK inside the declaration
    def get_block(decl):
        for child in decl.children:
            if child.type == 'block': return child
        return None

    config_vars_block = get_block(config_vars_decl)
    diagram_vars_block = get_block(diagram_vars_decl)
    
    if not config_vars_block or not diagram_vars_block:
        return diagram_code

    config_d2c_decl = find_key_in_block(config_vars_block, 'd2-config', config_code)
    if not config_d2c_decl:
        # Config has vars, but no d2-config. 
        # Should we merge other keys? The requirement focused on d2-config
        # But let's assume we do pure d2-config merge for now based on complexity.
        return diagram_code

    diagram_d2c_decl = find_key_in_block(diagram_vars_block, 'd2-config', diagram_code)
    
    # Case: Diagram vars exists, but d2-config missing inside it.
    if not diagram_d2c_decl:
        # Insert d2-config from config into diagram vars
        # Insert at start of vars block (after '{')
        to_insert = get_text_with_comment(config_d2c_decl, config_code, config_vars_block)
        insert_pos = diagram_vars_block.start_byte + 1
        return diagram_code[:insert_pos] + "\n  " + to_insert + diagram_code[insert_pos:]
        
    # Case: Both have d2-config. Merge keys.
    config_d2c_block = get_block(config_d2c_decl)
    diagram_d2c_block = get_block(diagram_d2c_decl)
    
    if not config_d2c_block or not diagram_d2c_block:
        return diagram_code

    # Identify missing keys
    to_insert_chunks = []
    
    # helper for existing keys
    existing_keys = set()
    for child in diagram_d2c_block.children:
        if child.type == 'declaration':
            k = get_key(child, diagram_code)
            if k: existing_keys.add(k)
            
    for child in config_d2c_block.children:
        if child.type == 'declaration':
            k = get_key(child, config_code)
            if k and k not in existing_keys:
                to_insert_chunks.append(get_text_with_comment(child, config_code, config_d2c_block))
                
    if not to_insert_chunks:
        return diagram_code
        
    # Insert keys at top of diagram d2-config block is cleaner
    insert_pos = diagram_d2c_block.start_byte + 1
    newline_indent = "\n    "
    insertion = newline_indent + newline_indent.join(to_insert_chunks)
    
    return diagram_code[:insert_pos] + insertion + diagram_code[insert_pos:]
