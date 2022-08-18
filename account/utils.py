import pyotp

def getotp():
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key,interval=360)
    otp = totp.now()
    return {"otp":otp, "key":key }

# def verifyotp(otp, key):
#     totp = pyotp.TOTP(key)
#     if totp.now()==otp:
#         return totp.verify(otp)
#     else:
#         return False