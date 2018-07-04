from PIL import Image
import os
import os.path
import glob
import cv2
import numpy as np

CAPTCHA_IMAGE_FOLDER = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\irct_nlpCatcha\\"
EDITED_CAPTCHA_IMAGE_FOLDER = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\irct_nlpCatcha_edited\\"
EDITED_CAPTCHA_IMAGE_FOLDER2 = "C:\\Users\\Honey\\Project\\Captcha_Detection\\Captch_Detection\\irct_nlpCatcha_edited2\\"

captcha_image_files = glob.glob(os.path.join(EDITED_CAPTCHA_IMAGE_FOLDER, "*"))

size = len(captcha_image_files)
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print('Processing image {} out of {}'.format (i + 1, size))
    filename = os.path.basename(captcha_image_file)
    captcha_correct_text = os.path.splitext(filename)[0]
    
    im = Image.open(captcha_image_file).convert('L')
    width, height = im.size
    im = im.crop((148, 0, width, height))
    im.save(EDITED_CAPTCHA_IMAGE_FOLDER + captcha_correct_text + '.png')
