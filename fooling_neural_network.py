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
from solve_captchas_with_model_irctc import predictImage
from solve_captchas_with_model_irctc import predictSingleImage


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

def displayImage(image):
    plt.imshow(image)
    plt.show()

with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)
    
model = load_model(MODEL_FILENAME)   

print(predictImage('pixel_attack\\3\\1_3W.png'))


img = cv2.imread('pixel_attack\\3.png')
indices = np.where(np.all(img != (255,255,255) , -1))
coords = list(zip(indices[0], indices[1]))
print(len(coords))

for index, coord in enumerate(coords):
    actual_letter = '2_folder'
    img = cv2.imread('pixel_attack\\3.png')
    x, y = coord
    img[x,y] = (170, 170, 170)
    predictions = predictImage('' ,img)
    if predictions != '3':
        print('Sucess in using one pixel manipulation predictions:' + predictions)
        ##cv2.imwrite('pixel_attack\\'+ actual_letter + '\\' + predictions + str(index) + '.png', img)
        #cv2.imwrite('C:\\Users\\Honey\\Project\\CaptchaDetection\\pixel_attack\\2\\' + predictions + str(index) + '\\.png' , img)
        cv2.imwrite('pixel_attack\\3\\' + str(index) + '_' + predictions + '.png', img)


gray = cv2.imread('pixel_attack\\2.png', cv2.COLOR_BGRA2GRAY)
displayImage(gray)
# Add some extra padding around the image
gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
displayImage(gray)
# threshold the image (convert it to pure black and white)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
displayImage(thresh)
# find the contours (continuous blobs of pixels) the image
#image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
_,contours,_ = cv2.findContours(thresh.copy(),  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



model_input_layer = model.layers[0].input
model_output_layer = model.layers[-1].output 

print(model_input_layer)
print(model_output_layer)


img = cv2.imread('C:\\Users\\Honey\\Project\\CaptchaDetection\\nlp_captcha_single\\1\\013.png')
displayImage(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
letter_image = resize_to_fit(gray, 20, 20)
letter_image = np.expand_dims(letter_image, axis=2)
letter_image = np.expand_dims(letter_image, axis=0)

original_image = letter_image

hacked_image = np.copy(original_image)
displayImage(hacked_image)
max_change_above = original_image + 0.01
max_change_below = original_image - 0.01

learning_rate = 0.1

# converting it into character I
object_type_to_fake = 18
# Define the cost function.
# Our 'cost' will be the likelihood out image is the target class according to the pre-trained model
cost_function = model_output_layer[0, object_type_to_fake]

# We'll ask Keras to calculate the gradient based on the input image and the currently predicted class
# In this case, referring to "model_input_layer" will give us back image we are hacking.
gradient_function = K.gradients(cost_function, model_input_layer)[0]

# Create a Keras function that we can call to calculate the current cost and gradient
grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function, gradient_function])

cost = 0.0
hacked_image = hacked_image.astype(np.float32)
while cost < 0.50:
    # Check how close the image is to our target class and grab the gradients we
    # can use to push it one more step in that direction.
    # Note: It's really important to pass in '0' for the Keras learning mode here!
    # Keras layers behave differently in prediction vs. train modes!
    cost, gradients = grab_cost_and_gradients_from_model([hacked_image, 0])
    
    # Move the hacked image one step further towards fooling the model
    hacked_image += gradients * learning_rate
    
    # Ensure that the image doesn't ever change too much to either look funny or to become an invalid image
    #hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
    #hacked_image = np.clip(hacked_image, -1.0, 1.0)

    print("Model's predicted likelihood that the image is a charater I: {:.8}%".format(cost * 100))
    
img = hacked_image[0]
img  = img.astype(np.uint8)
cv2.imwrite('hacked.png', img)

from solve_captchas_with_model_irctc import predictImage

letter = predictImage('hacked image\\001_3.png')
print(letter)