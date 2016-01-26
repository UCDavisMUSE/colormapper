# Colormapper

## About

This program is a tool for converting fluorescent microscopy images into images that mimic brightfield microscopy. This allows images taken with fluorescent dyes and staines to be converted into images resembling standard histological slides that use, for example, the H&E (hematoxylin and eosin) stain combination. 

This program is written in Python 2.7 using wxPython 3.0.2.0.

## Authors

Zachary T. Harmany, PhD
zharmany@gmail.com

## Issues & Feature Requests

### Pending

- Localize menu items and keyboard shortcuts for Windows.
- Check to see if the use of Accelerator Menus would aid in localization efforts. See the blog posts [here](http://www.blog.pythonlibrary.org/2010/12/02/wxpython-keyboard-shortcuts-accelerators/) and [here](http://www.blog.pythonlibrary.org/2008/07/02/wxpython-working-with-menus-toolbars-and-accelerators/).
- History of computed colormappings in a panel with image thumbnails. This is temporary and is purged upon closing.
- Clipboard functionality.
- Undo / Redo functionality.
- Disable export menu item if no image has been converted.
- Check if threads can be used for saving, and applying the colormap. This should help the UI be more responsive.
- Investigate faster methods to save large image files, especially PNG files
- In Windows, double check that the open / save / import / export dialog boxes open to the directory of the last successful open / save / import / export operation. 
- Batch processing.
- Take the colormapping code off the main thread.

### Finished

- [DONE: Simply added the name of the original image in the title bar] Add the name of the image (perhaps instead of the colormapper file) in the title bar. Perhaps adding an asterisk if not imported with the current settings.
- [Fixed] Double check that it works on drop target.
- [DONE: Use cPickle] Determine format for saving color conversion settings.
- [DONE: Save / Open loads the input and output colors] Method to simply import / export the algorithm settings (as to apply to a new image without needing to load the source image and mapped image).
- [DONE] Upon Import/Export or Open/Save, ensure the current working directory gets updated so that a user does not need to re-navigate to the directory. This may need to be done with the os python module, since os.getcwd() gets the current working directory.
- [DONE] Related to the above, populate the save dialog box with the current file name if previously saved.
- [FIXED] Bug: When importing an image with the same dimensions as the current image, the input image panel does not refresh. This is because I resize the image to fit the panel within the GetImageDisplaySize method of the ImageViewerPanel class, and skip resizing if the dimensions don't change to save on CPU cycles. 
- [ADDED] Feature: Be able to specify the number of selected colors. 
- [DONE] Drag and drop image to open functionality.

### For Unmix Branch

- Try to refactor code a bit better, easy spots:
    - Slider plus spinner plus textbox controls as one item
    - methods to set color of color box and spectrum
- If sticking with Open CL unmix, stop shuttling info to/from GPU
- Fastest way to get image displayed onto screen (Do remix in wx.Image domain?)
- Toolbar for zoom / pan controls on the images
- [Done] Save / load settings (perhaps a separate settings class, add save / load settings methods)
- Code to grab color from image using crosshairs. 
- Way to launch colormapper importing a particular image (for Farzad command line).
- Try to get working correctly on windows.
- Get unmix and remix off the main thread.
- [Done] Create a settings class:
    - Use a dictionary for the settings (so that they can be easily saved and loaded)
    - Create get and set methods, this is useful so that SetNucleiColor updates the spectrum automatically, and accounts for background subtraction.
- Perhaps use YAML as a saving format for the settings.