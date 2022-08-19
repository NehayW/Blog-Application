import pyotp

def getotp():
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key,interval=360)
    otp = totp.now()
    return {"otp":otp, "key":key }
