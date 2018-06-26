# CaptchDetection

Captcha is a system used to stop bots or automatic software to access the site. IRCTC is a popular travel website in india where people book travel tickets on trains. Because of high demand of tickets, booking during peak hours (tatkal) has a captcha image containing letters that humans have to enter to book the ticket. This supposedly stops ticket booking through automated software. But with use of Deep learning this can be acheived.

Irctc used three types of captcha image on its website 

1) Simple Captcha:

<img src= "\captcha_images\simple captcha.png" width="400" alt="simple captcha">
</br>

2) Coloring Captcha:

<img src= "\captcha_images\Color captcha.png" width="400" alt="Color Captcha">
</br>


3) Complex Captcha :


Files Description:

i) irctc_web-scrapping
	For downloading simple captcha through weblink.

ii) selenium_download
	For downloading color and complex captcha through selenium webdriver.

iii) cropping_irctc_images
	
	In case of color captcha images, it starts with "Type in box below:" we crop that images and save it.

iv) extract_single_letters_from_captcha

	After creating captcha images database, letters from captcha is extracted and stored in their respective folder.


v) train_model
	
	We are using keras framework for building model and we are using 4 convolution layer. 


vi) captcha_model.hdf5
	
	After training the model we save the model in this file.

vii)	model_labels.dat

	We stored all the labels value in this file.

viii) solve_captcha_with_model

	This file is used for predicting captcha image label.

ix) new_irctc_login
	
	It contains code for booking ticket on irctc.

x)	google_service.json, firebase_remote_config, firebase_database_access

	All the files are related with firebase	

