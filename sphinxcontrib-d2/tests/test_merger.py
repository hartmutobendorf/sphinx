
import pytest
from sphinxcontrib.d2.merger import merge_d2_content
from pathlib import Path

@pytest.mark.parametrize("diagram_file, merged_file", [
    ("diagram1.d2", "merged1.d2"),
    ("diagram2.d2", "merged2.d2"),
])
def test_d2_merge_logic(diagram_file, merged_file):
    # Load files from data dir
    data_dir = Path(__file__).parent / 'data'
    
    diagram_content = (data_dir / diagram_file).read_text()
    config_content = (data_dir / 'config.d2').read_text()
    expected_content = (data_dir / merged_file).read_text()
    
    # Perform merge
    merged = merge_d2_content(diagram_content, config_content)
    
    assert merged.strip() == expected_content.strip()
