# Colormapper

## About

This program is a tool for converting fluorescent microscopy images into images that mimic brightfield microscopy. This allows images taken with fluorescent dyes and staines to be converted into images resembling standard histological slides that use, for example, the H&E (hematoxylin and eosin) stain combination. 

This program is written in Python 2.7 using wxPython 3.0.2.0.

Please let us know if there are features that would be useful for your research.

## Authors

Zachary T. Harmany, PhD
zharmany@gmail.com

## List of issues and feature requests

- Localize menu items and keyboard shortcuts for Windows.
- Check to see if the use of Accelerator Menus would aid in localization efforts. See the blog posts [here](http://www.blog.pythonlibrary.org/2010/12/02/wxpython-keyboard-shortcuts-accelerators/) and [here](http://www.blog.pythonlibrary.org/2008/07/02/wxpython-working-with-menus-toolbars-and-accelerators/).
- History of computed colormappings in a panel with image thumbnails. This is temporary and is purged upon closing.
- Undo / Redo functionality.
- Disable export menu item if no image has been converted.
- Use thread for converting entire image then saving. This should help the UI be more responsive.
- Investigate faster methods to save large image files, especially PNG files
- In Windows, double check that the open / save / import / export dialog boxes open to the directory of the last successful open / save / import / export operation. 
- Batch processing.
- Take the colormapping code off the main thread.
- Try to refactor code a bit better, easy spots:
    - Slider plus spinner plus textbox controls as one item
    - methods to set color of color box and spectrum
- If sticking with Open CL unmix, stop shuttling info to/from GPU
- Fastest way to get image displayed onto screen (Do remix in wx.Image domain?)
- Way to launch colormapper importing a particular image (for Farzad command line).
- Perhaps use YAML as a saving format for the settings.


