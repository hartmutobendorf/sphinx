"""
sphinxcontrib.d2
~~~~~~~~~~~~~~~~

Sphinx extension for rendering D2 diagrams.
"""

import subprocess
import os
import shutil
import hashlib
import posixpath
import tempfile
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.errors import SphinxError
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset
from .merger import merge_d2_content

logger = logging.getLogger(__name__)

__version__ = '0.1.0'

class D2Error(SphinxError):
    category = 'D2 error'

class d2_node(nodes.General, nodes.Inline, nodes.Element):
    pass

class D2Directive(SphinxDirective):
    """Directive to insert D2 diagrams."""
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
        'align': directives.unchanged,
        'caption': directives.unchanged,
        'file': directives.unchanged,
    }

    def run(self):
        node = d2_node()
        
        if 'file' in self.options:
            rel_filename, filename = self.env.relfn2path(self.options['file'])
            self.env.note_dependency(rel_filename)
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    node['code'] = f.read()
            except (IOError, OSError):
                return [self.state.document.reporter.warning(
                    'External D2 file %r not found or reading it failed' % filename,
                    line=self.lineno)]
        else:
            node['code'] = '\n'.join(self.content)
            if not node['code'].strip():
                return [self.state.document.reporter.warning(
                    'Ignoring "d2" directive without content.',
                    line=self.lineno)]

        node['options'] = self.options

        if 'caption' in self.options:
            align = self.options.get('align')
            figure_node = nodes.figure('', align=align)
            figure_node += node
            
            caption_text = self.options['caption']
            text_nodes, _ = self.state.inline_text(caption_text, self.lineno)
            caption_node = nodes.caption(caption_text, '', *text_nodes)
            figure_node += caption_node
            
            return [figure_node]
        else:
            if 'align' in self.options:
                node['align'] = self.options['align']
            return [node]

def copy_static_files(app, exc):
    if app.builder.format == 'html' and not exc:
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        out = os.path.join(app.builder.outdir, '_static')
        copy_asset(static_dir, out)

def render_d2(self, code, options, format='svg'):
    d2_cmd = self.builder.config.d2_command
    d2_config_file = self.builder.config.d2_config
    
    full_code = code
    if d2_config_file:
        try:
            config_path = os.path.join(self.builder.confdir, d2_config_file)
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                    full_code = merge_d2_content(code, config_content) 
            else:
                logger.warning(f'd2_config file {d2_config_file} not found')
        except Exception as e:
            logger.warning(f'Failed to read d2_config file: {e}')

    hashopts = (
        full_code + 
        str(options) + 
        d2_cmd + 
        str(d2_config_file) + 
        format + 
        str(self.builder.config.d2_font) + 
        str(self.builder.config.d2_mono_font)
    )
    hashed = hashlib.sha1(hashopts.encode('utf-8')).hexdigest()
    
    fname_base = f'd2-{hashed}'
    outdir = self.builder.outdir
    env = os.environ.copy()

    def run_d2(args, output_path):
        # Create a temp file for d2 input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.d2', delete=False, encoding='utf-8') as tf:
            tf.write(full_code)
            temp_path = tf.name

        cmd = [d2_cmd] + args + [temp_path, output_path]
        
        if self.builder.config.d2_font:
             cmd.insert(len(cmd)-2, f'--font-regular={self.builder.config.d2_font}')
        if self.builder.config.d2_mono_font:
             cmd.insert(len(cmd)-2, f'--font-mono={self.builder.config.d2_mono_font}')
             
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                env=env
            )
        except OSError:
            raise D2Error(f'd2 command {d2_cmd!r} cannot be run')
        except subprocess.CalledProcessError as exc:
            raise D2Error(f'd2 exited with error:\n{exc.stderr.decode("utf-8")}')
#        finally:
#            if os.path.exists(temp_path):#
#                os.remove(temp_path)

    if format == 'svg':
        fname_light = f'{fname_base}-light.svg'
        fname_dark = f'{fname_base}-dark.svg'
        
        img_dir = os.path.join(outdir, '_images')
        os.makedirs(img_dir, exist_ok=True)
        
        abs_light = os.path.join(img_dir, fname_light)
        abs_dark = os.path.join(img_dir, fname_dark)
        
        if not os.path.exists(abs_light):
            run_d2(['--theme=0'], abs_light)
            
        if not os.path.exists(abs_dark):
            run_d2(['--theme=200'], abs_dark)

        return [fname_light, fname_dark]

    elif format == 'pdf':
        fname = f'{fname_base}.pdf'
        abs_path = os.path.join(outdir, fname)
        
        if not os.path.exists(abs_path):
             run_d2(['--theme=0'], abs_path)
             
        return fname

def html_visit_d2(self, node):
    try:
        filenames = render_d2(self, node['code'], node['options'], format='svg')
    except D2Error as exc:
        logger.warning('d2 rendering failed: ' + str(exc))
        raise nodes.SkipNode

    fname_light, fname_dark = filenames
    
    def make_img(fname, cls):
        path = posixpath.join(self.builder.imgpath, fname)
        alt = node.get('alt', '')
        return f'<img src="{path}" class="{cls}" alt="{alt}" />'

    div_start = '<div class="d2-figure">'
    img_light = make_img(fname_light, 'd2-light')
    img_dark = make_img(fname_dark, 'd2-dark')
    div_end = '</div>'
    
    self.body.append(div_start + img_light + img_dark + div_end)
    raise nodes.SkipNode

def latex_visit_d2(self, node):
    try:
        fname = render_d2(self, node['code'], node['options'], format='pdf')
    except D2Error as exc:
        logger.warning('d2 rendering failed: ' + str(exc))
        raise nodes.SkipNode
        
    self.body.append(r'\sphinxincludegraphics[]{%s}' % fname)
    raise nodes.SkipNode

def setup(app):
    app.add_node(d2_node, html=(html_visit_d2, None), latex=(latex_visit_d2, None))
    app.add_directive('d2', D2Directive)
    
    app.add_config_value('d2_command', 'd2', 'env')
    app.add_config_value('d2_config', None, 'env')
    app.add_config_value('d2_font', None, 'env')
    app.add_config_value('d2_mono_font', None, 'env')
    
    app.connect('build-finished', copy_static_files)
    app.add_css_file('d2.css')
    app.add_js_file('d2.js')
    
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

