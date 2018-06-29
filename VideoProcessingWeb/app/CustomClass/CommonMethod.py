import base64
import codecs
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

class CommonMethod(object):
      """description of class"""
def LinkLogin(LoginStr):
    bytesString = LoginStr.encode(encoding="utf-8")
    bytesString = base64.b64decode(bytesString)
    LoginStr = str(bytesString, encoding = "utf-8")  
    UserName = LoginStr.split("_")[0]
    PassWord = LoginStr.split("_")[1]
    user = authenticate(username=UserName,password=PassWord)
    if user:
        return user
    else:
        return False