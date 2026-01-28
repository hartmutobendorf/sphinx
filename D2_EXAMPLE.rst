Sphinx D2 Extension Example
===========================

This example demonstrates how to use the `sphinxcontrib-d2` extension to embed D2 diagrams in your Sphinx documentation.

Prerequisites
-------------

1.  Install the extension:

    .. code-block:: bash

        pip install sphinxcontrib-d2

2.  Ensure the `d2` CLI tool is installed (https://d2lang.com/tour/install).

Configuration
-------------

Add ``sphinxcontrib.d2`` to your ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinxcontrib.d2',
       # ...
   ]

   # Optional: Path to a global D2 configuration file
   d2_config = 'd2_config.d2'

Usage
-----

You can use the ``.. d2::`` directive in two ways.

1. Inline Diagram
^^^^^^^^^^^^^^^^^

Write D2 code directly in your reStructuredText file:

.. d2::
   :caption: A Simple Connection

   x -> y: hello world

2. External File
^^^^^^^^^^^^^^^^

Reference an external ``.d2`` file:

.. d2::
   :file: diagrams/architecture.d2
   :caption: System Architecture

Advanced Features
-----------------

Configuration Merging
^^^^^^^^^^^^^^^^^^^^^
If you define a global ``d2_config`` in ``conf.py``, its settings (like themes, sketch mode, layout engines) are automatically merged into your diagrams.

*   Diagram-specific settings take precedence.
*   Unique settings from the global config are added.

For example, if your global config sets ``theme-id: 3`` (Terrastruct), all diagrams will use that theme unless they explicitly set a different one.

Output Formats
^^^^^^^^^^^^^^
The extension automatically handles:

*   **HTML**: Generates both Light and Dark mode SVGs and switches them dynamically using CSS.
*   **LaTeX/PDF**: Generates PDF vector graphics for high-quality print output.
