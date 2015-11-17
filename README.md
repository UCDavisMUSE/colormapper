# Colormapper

## About

This program is a tool for converting fluorescent microscopy images into images that mimic brightfield microscopy. This allows images taken with fluorescent dyes and staines to be converted into images resembling standard histological slides that use, for example, the H&E (hematoxylin and eosin) stain combination. 

This program is written in Python 2.7 using wxPython 3.0.2.0.

## Authors

Zachary T. Harmany, PhD
zharmany@gmail.com

## Issues & Feature Requests

- Localize menu items and keyboard shortcuts for Windows.
- [DONE: Use cPickle] Determine format for saving color conversion settings.
- Check to see if the use of Accelerator Menus would aid in localization efforts. See the blog posts [here](http://www.blog.pythonlibrary.org/2010/12/02/wxpython-keyboard-shortcuts-accelerators/) and [here](http://www.blog.pythonlibrary.org/2008/07/02/wxpython-working-with-menus-toolbars-and-accelerators/).
- [DONE: Save / Open loads the input and output colors] Method to simply import / export the algorithm settings (as to apply to a new image without needing to load the source image and mapped image).
- Upon Import/Export or Open/Save, ensure the current working directory gets updated so that a user does not need to re-navigate to the directory. This may need to be done with the os python module, since os.getcwd() gets the current working directory.
- [FIXED] Bug: When importing an image with the same dimensions as the current image, the input image panel does not refresh. This is because I resize the image to fit the panel within the GetImageDisplaySize method of the ImageViewerPanel class, and skip resizing if the dimensions don't change to save on CPU cycles. 
- [ADDED] Feature: Be able to specify the number of selected colors. 
- History of computed colormappings in a panel with image thumbnails. This is temporary and is purged upon closing.
- Clipboard functionality.
- Undo / Redo functionality.
- Drag and drop image to open functionality.