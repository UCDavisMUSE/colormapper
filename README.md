# Colormapper

## About

This program is a tool for converting fluorescent microscopy images into images that mimic brightfield microscopy. This allows images taken with fluorescent dyes and staines to be converted into images resembling standard histological slides that use, for example, the H&E (hematoxylin and eosin) stain combination. 

This program is written in Python 2.7 using wxPython 3.0.2.0.

## Authors

Zachary T. Harmany, PhD
zharmany@gmail.com

## Issues & Feature Requests

- Localize menu items and keyboard shortcuts for Windows.
- Determine format for saving color conversion settings.
- Check to see if the use of Accelerator Menus would aid in localization efforts. See the blog posts [here](http://www.blog.pythonlibrary.org/2010/12/02/wxpython-keyboard-shortcuts-accelerators/) and [here](http://www.blog.pythonlibrary.org/2008/07/02/wxpython-working-with-menus-toolbars-and-accelerators/).
- Method to simply import / export the algorithm settings (as to apply to a new image without needing to load the source image and mapped image).