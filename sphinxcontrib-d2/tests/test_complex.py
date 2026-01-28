
import pytest
import shutil
import os

@pytest.mark.sphinx('html', testroot='complex')
def test_d2_file_argument(app, status, warning):
    # Retrieve the source dir
    srcdir = app.srcdir
    print(f"Source directory: {srcdir}")
    outdir = app.outdir
    print(f"Output directory: {outdir}")

    assert srcdir.exists()
    
    # Modify index.rst to replace marker with directive
    index_file = srcdir / 'index.rst'
    content = index_file.read_text()
    
    # Inject d2 directive using external file
    directive = """
.. d2::
   :file: diagram1.d2
"""
    new_content = content.replace('***DIAGRAM HERE***', directive)
    index_file.write_text(new_content)
    
    # Build
    try:
        app.build()
    except Exception as e:
        pytest.fail(f"Build failed: {e}")
    
    # Check for build warnings
    assert not warning.getvalue().strip()
    
    # Check output
    out_file = app.outdir / 'index.html'
    assert out_file.exists()
    content = out_file.read_text()
    assert 'd2-figure' in content
    assert '<img src="_images/d2-' in content
    
    # Check if the svg files are created
    images_dir = app.outdir / '_images'
    assert images_dir.exists()
    svgs = list(images_dir.glob('d2-*.svg'))
    assert len(svgs) >= 2 # light and dark


@pytest.mark.sphinx('html', testroot='complex', confoverrides={'d2_config': 'config.d2'})
def test_d2_config_prepend(app, status, warning):
    # Retrieve the source dir
    srcdir = app.srcdir
    
    # Modify index.rst 
    index_file = srcdir / 'index.rst'
    content = index_file.read_text()
    
    # Inject d2 directive with inline code
    directive = """
.. d2::

   x -> y
"""
    new_content = content.replace('***DIAGRAM HERE***', directive)
    index_file.write_text(new_content)
    
    # Build
    try:
        app.build()
    except Exception as e:
        pytest.fail(f"Build failed: {e}")
    
    assert not warning.getvalue().strip()
    
    content = (app.outdir / 'index.html').read_text()
    assert 'd2-figure' in content
    
    # Optional: Verify that the output differs when d2_config is used (hard to do without a baseline).
    # But ensuring it builds without error when d2_config is set is the primary goal here.
