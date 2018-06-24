import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://captchadetection-8351e.firebaseio.com/'
})

root = db.reference()
def updateOtp(otp):
    root.child('paytm').update({
            'otp' : otp
    })

def updateSession(status):
    root.child('paytm').update({
            'session' : status
    })

def getOtp():
    value = root.child('paytm').get('otp')
    otp = value[0]['otp']
    return otp

updateOtp(500)
updateSession(False)
otp = getOtp()
print(otp)
