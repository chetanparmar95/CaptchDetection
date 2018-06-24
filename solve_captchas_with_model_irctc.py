import os
import os.path
import cv2
import glob
import imutils
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from keras.models import load_model
#from helpers import resize_to_fit
from imutils import paths
import imutils
import pickle
from keras import backend as K

main_folder = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\"
main_folder = "E:\\Aagam\\Project\\solving_captchas_code_examples\\solving_captchas_code_examples\\"
CAPTCHA_IMAGE_FOLDER = main_folder + "\\irctc_images\\Letter Captcha\\"
OUTPUT_FOLDER = main_folder + "extracted_irctc_image\\"

# Get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))

counts = {}

#print(len(captcha_image_files))

MODEL_FILENAME = main_folder + "captcha_model.hdf5"
MODEL_LABELS_FILENAME = main_folder + "model_labels.dat"
CAPTCHA_IMAGE_FOLDER = main_folder + "generated_captcha_images"

def resize_to_fit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """

    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]

    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)

    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image

# Load up the model labels (so we can translate model predictions to actual letters)
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)
    
model = load_model(MODEL_FILENAME)   

#from keras.utils import plot_model
#import pydot
#import graphviz
#plot_model(model, to_file='model.png')

    
def readAlphaIamge(filePath):
    image = Image.open(filePath)
    bg = Image.new('RGB', image.size, (255, 255, 255))
    bg.paste(image, (0, 0), image)
    return bg
    # Save pasted image as image
    #bg.save(TMP_FILE)
    
def displayImage(image):
    plt.imshow(image)
    plt.show()

EDITED_CAPTCHA_IMAGE_FOLDER2 = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\irct_nlpCatcha_edited2\\"
EDITED_CAPTCHA_IMAGE_FOLDER3 = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\irct_nlpCatcha_edited3\\"

def predictSingleImage(imagePath, img = None):

    if img is None:
    #print(captcha_image_file)
    #print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
        filename = os.path.basename(imagePath)
        image = cv2.imread(imagePath)
    else:
        image = img
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
    letter_image = gray
    # Get the folder to save the image in
    #displayImage(letter_image)
    # Re-size the letter image to 20x20 pixels to match training data
    letter_image = resize_to_fit(letter_image, 20, 20)
    # Turn the single image into a 4d list of images to make Keras happy
    letter_image = np.expand_dims(letter_image, axis=2)
    letter_image = np.expand_dims(letter_image, axis=0)
    
    #print(letter_image)
    # Ask the neural network to make a prediction
    prediction = model.predict(letter_image)
    # Convert the one-hot-encoded prediction back to a normal letter
    predictions = lb.inverse_transform(prediction)[0]
    return predictions

def predictImage(imagePath, img = None):

    if img is None:
    #print(captcha_image_file)
    #print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
        filename = os.path.basename(imagePath)
        image = cv2.imread(imagePath)
    else:
        image = img
    #image = img
    #displayImage(image)
    #print(image.shape)
    #image = np.array(readAlphaIamge(captcha_image_file))
    # Loading the image and converting it into grayscale
    #image = cv2.imread(TMP_FILE)
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    #displayImage(gray)
    # Add some extra padding around the image
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
    #displayImage(gray)
    # threshold the image (convert it to pure black and white)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #displayImage(thresh)
    # find the contours (continuous blobs of pixels) the image
    #image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _,contours,_ = cv2.findContours(thresh.copy(),  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    letter_image_regions = []

    equalSignContourPosition = [] 
    contourList = []
    equalSignExist = False

    for indexi, contouri in enumerate(contours):
        (xi, yi, wi, hi) = cv2.boundingRect(contouri)
        for indexj, contourj in enumerate(contours):
            if indexj != indexi:

                (xj, yj, wj, hj) = cv2.boundingRect(contourj)
                if xi == xj and wi == wi and hi == hj:
                    if not(indexi in equalSignContourPosition) : 
                        #print('adding')
                        letter_image_regions.append((xi, min(yi,yj) , wi, hi + hj + abs(yi - yj)))
                        contourList.append(contouri)
                        contourList.append(contourj)
                        equalSignContourPosition.append(indexi)
                        equalSignContourPosition.append(indexj)
                        equalSignExist = True
                        break

    #print('equalSignContourPosition:' + str(equalSignContourPosition))
    for index, contour in enumerate(contours):
        if not(index in equalSignContourPosition):
            #print('adding in letter image region:' + str(index))
            letter_image_regions.append(cv2.boundingRect(contour))

    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
    predictions = ''
    #try:
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box
        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]
        # Get the folder to save the image in
        #displayImage(letter_image)
        # Re-size the letter image to 20x20 pixels to match training data
        letter_image = resize_to_fit(letter_image, 20, 20)
        # Turn the single image into a 4d list of images to make Keras happy
        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)
        
        #print(letter_image)
        # Ask the neural network to make a prediction
        prediction = model.predict(letter_image)
        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb.inverse_transform(prediction)[0]
        predictions+= letter
    #except:
    #    print('error' + filename)
    #cv2.imwrite(EDITED_CAPTCHA_IMAGE_FOLDER3 + predictions + '.png',image)
    
    return predictions
        #print(predictions)
    
        #print(main_folder + 'irctc\\annotation_Testing\\'+ predictions + '.png')
        #cv2.imwrite(main_folder + 'irctc_images\\annotation_Testing\\'+ predictions + '.png', image)

  
      
'''import os
import os.path
import glob
import cv2

captcha_image_files = glob.glob(os.path.join(EDITED_CAPTCHA_IMAGE_FOLDER2, "*"))        
predictImage(captcha_image_files)
        
import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread('000590.png')
image[np.where((image > (150,150,150)).all(axis = 2))] = [255,255,255]
cv2.imwrite('3.png', image)

img[]
print(img[4, 36])
dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
cv2.imwrite('1.png', dst)
plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(dst)
plt.show()'''