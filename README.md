### ADS2014 Final Project

This project was assigned as an introduction to image processing in Python.

Thanks to [Dr. Greg Dobler](https://github.com/gdobler/ads14) for a good module and lots of Python practice.

#### Files

1. image_manipulation.py 
  * A simple script that performs some basic manipulations on an image of the Mona Lisa

2. image_exploration_combined.py
  * An interactive tool for exploring image histograms. 
  * Clicking twice in the image will select a rectangular region and display the histogram for that region. 
  * Double clicking resets tothe histogram of the whole image. 
  * Clicking in the histogram will select a 11-pixel wide window for that color. Choosing a window 
    in r, g, & b will dim by 75% all pixels in the image that do not fall in the window.
    
3. regression_accuracy.py
  * Performs naive character recognition by regressing each image in the dataset against averaged
    templates for each digit type (0-9) using OLS. 
  * The template with the highest regression coefficient is chosen as the match.
  * Displays histograms of regression coefficients for each digit.
  * Prints accuracy statistics.
  * Plays a 30s video displaying randomly chosen examples of incorrect matches.
