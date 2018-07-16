import base64
import codecs
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import time
import datetime

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

def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st
