'''
Created on Feb 19, 2023

@author: bradenhicks
'''

import cv2
import numpy as np 


def detectCones(image):
    im = image
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    grey = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY) #change to greyscale
    blurred = cv2.blur(grey, (7,7))
    eroded = cv2.erode(blurred, (7,7), iterations=11)
    mask = cv2.inRange(eroded, 190, 255) #only keep pixels in range, white = in range, black = not
    
    return mask


def extendLines(image, pointA, pointB, distance=10000):
    im = image
    a = pointA
    b = pointB
    dist = distance
    slope = np.arctan2(b[1] - a[1], b[0] - a[0])
    
    #Find end points - these are off the screen along
    # the same slope
    bigAX = int(a[0] + dist*np.cos(slope))
    bigAY = int(a[1] + dist*np.sin(slope))
    bigBX = int(b[0] - dist*np.cos(slope))
    bigBY = int(b[1] - dist*np.sin(slope))
    
    bigA = (bigAX,bigAY)
    bigB = (bigBX,bigBY)
    
    im = cv2.line(im, bigA, bigB, (0,255,0), 3)
    return im 
    
    


def createPoints(maskedIm, finalIm):
    im = maskedIm
    left = []
    right = []
    contours,_ = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        #Find center of the contours (the cones)
        x, y, w, h = cv2.boundingRect(c)
        centerX = int(x + 0.5 * w)
        centerY = int(y + 0.5 * h)
        width = im.shape[1]
        
        #separate the left and right points to create intersecting lines
        if(centerX > width/2):
            right.append((centerX,centerY))
        else:
            left.append((centerX,centerY))
            
    
    npLeft = np.array(left)
    npRight = np.array(right)
    '''
    Keep the first 3 cones, this way we do not include
    cones too far ahead
    Reasoning: The path is made of two lines.
               Imagine a curved road, path would be affected
               by cones too far down the line
    Alternate Idea: draw a line between each point, that way 
                    we can account for curves
                    However, might be inefficient when driving,
                    as it would constantly redraw lines for 
                    each cone
    '''
    startLeft = npLeft[0:3]
    startRight = npRight[0:3]

    #Draw lines
    finalIm = extendLines(finalIm, startLeft[0], startLeft[2])
    finalIm = extendLines(finalIm, startRight[0], startRight[2])
    return finalIm
    
    
def main():
    im = cv2.imread("green.png")
    maskedIm = detectCones(im)
    finalIm = createPoints(maskedIm, im)
    
    cv2.imshow("Cones Detected", finalIm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
main()
     
    
    
    
    



    