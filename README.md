# License Plates Detecting App

This application is designed to process images and extract license plate as a text.

## Libraries used:
 - OpenCV: OpenCV is a computer vision library that provides various image processing functions.
   It is used in this application to perform image manipulation and extraction of license plate regions.
   The benefits of using OpenCV include its extensive set of image processing algorithms and its
   compatibility with multiple programming languages.

 - Tesseract OCR: Tesseract OCR is an optical character recognition engine that is used to recognize
   text from images. In this application, Tesseract OCR is used to extract the license plate number
   from the license plate region identified by OpenCV. The benefits of using Tesseract OCR include
   its accuracy in recognizing text from images and its support for multiple languages.

## Extracting potential license plate images
 1. User upload image and it is saved as Python Imaging Library Image then converted to grayscale
 2. Image is preprocessed one of 3 methods, which are called in order from most common case to the more specific.  
 For example: *if the license plate has been found after processing image with 1 method then program print result and methods 2, 3 would not be called. Otherwise, if license plate text couldn't been found then app try to process it with next method and then detect license plate number*.  
 Description of methods which are used to process image is available in the next point.
 3. Using OpenCV's contour detection objects are extracted from the image. 
 4. Objects are processed and saved to set of unique elements: only objects which are parents are preserved.  
 *Note: if we are looking for license plate then we are sure that each license plate constins child objects in the form of  characters.* 
 5. We are iterating over list of parents elements. If element has exactly 4 vertices then:
    - mask to crop the image is created
    - mask is applied to image and as a result we can save cropped image containing only possible license plate to file
 6. Iterating over each image saved in the previous point we are trying to detect license plate text. If license plate text is detected then program print it and stop processing further images.

## Methods used for image transformation
As it was metioned in the previous point there are 3 methods which try to prepare image to be processed by text detecting algorithm.
1. Method 1(most commonly used) - it consist of 3 steps:
    - **bilateral filter:** it is non-linear, edge-preserving, and noise reducing smoothing filter. It particulary smooth image while preserving edges and as a effect removes noise from the photo.
    - **threshold using Otsu's method with tozero:** the image is converted to monochrome using threshold value got from Otsu's method and TOZERO technique.
    - **adaptiveThreshold** image is converted to binary and inverted using filter which adjust thresholding to neighbourhood of the pixels
2. Method 2:
    - **bilateral filter:** it is non-linear, edge-preserving, and noise reducing smoothing filter. It particulary smooth image while preserving edges and as a effect removes noise from the photo.
    - **threshold using Otsu's method with tozero:** Utilizes Otsu's method to automatically determine an optimal threshold.
    - **Canny edge detection** applies the Canny edge detection algorithm to the filtered and thresholded image(threshold detected in previous step is used).
2. Method 3:
    - **bilateral filter:** it is non-linear, edge-preserving, and noise reducing smoothing filter. It particulary smooth image while preserving edges and as a effect removes noise from the photo.
    - **threshold using Otsu's method with tozero:** Utilizes Otsu's method to automatically determine an optimal threshold.
    - **Laplacian edge detection** utilizes the Laplacian operator for edge detection on the image filtered with a bilateral filter which highlights regions of rapid intensity change, emphasizing edges and fine details in the image.



 ## Responsibilities
 Each of contributors was responsible for the following part of project:
 1. **Kacper Tracz** - prepared GUI for the app
 2. **Jakub Mikusek** - created mechanism of preparing image to be proceeded by text detection algorithm
 3. **Miłosz Trzop** - created mechanism of detecting text on extracted license plate images
 4. **Krzysztof Czerwiński** - prepared the documentation

 ## 
