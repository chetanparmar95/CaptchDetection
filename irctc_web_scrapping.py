# Simple Capcha download

import requests
print(str(10).zfill(5))
main_folder = '\\irctc images\\'

for i in range(1,10):
    print("Progress:" + str(i) )
    filedata = requests.get('https://www.irctc.co.in/eticketing/captchaImage?0.8083772336514661')
    
    with open(main_folder + str(i).zfill(5) + '.png', 'wb') as f:  
        f.write(filedata.content)