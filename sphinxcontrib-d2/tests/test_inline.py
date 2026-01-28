
import pytest
from pathlib import Path

@pytest.mark.sphinx('html', testroot='inline')
def test_d2_inline_doc3(app, status, warning):
    # Retrieve the source dir
    srcdir = app.srcdir
    
    # Copy doc3.rst content to index.rst
    data_dir = Path(__file__).parent / 'data'
    doc3_content = (data_dir / 'doc3.rst').read_text()
    
    index_file = srcdir / 'index.rst'
    index_file.write_text(doc3_content)
    
    # Build
    try:
        app.build()
    except Exception as e:
        pytest.fail(f"Build failed: {e}")
    
    assert not warning.getvalue().strip()
    
    content = (app.outdir / 'index.html').read_text()
    assert 'd2-figure' in content
    assert 'caption one' in content
    
    # Check images existence
    images_dir = app.outdir / '_images'
    assert len(list(images_dir.glob('d2-*.svg'))) >= 2
    
