# WACodingChallenge

PNGs are attached with the original and modified version

Methodology:
The goal was to first detect only the cones in the image.
Then, collapse each cones to a singular point in order to draw lines.
Split the points down the vertical axis of the image, so that we 
  could create left and right boundaries 
I chose to keep only the first 4 points from each side:
  This is because I felt that anything more than 4 or 5 points would affect the path
  I tried to imagine cones laid out while driving - they usually aren't perfectly straight, 
  so I couldn't keep all points. I originalltried to keep all the points, but since the cones 
  weren't straight I cut the last few points.
I also tried to draw individual line segments to each cone and then extend the lines,
but that was very slow.

Libraries:
- OpenCV (import cv2)
- NumPy (import numpy as np) 


