# importing the requests library
import requests
import re
import hashlib
import urllib.parse

# api-endpoint
URL = "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI"

def getCookie():
    r = requests.get('https://www.cleverbot.com/extras/conversation-social-min.js')
    # cookie = r.headers['Set-cookie']
    match = re.findall("md5\([^)]+substring\((\d+),(\d+)\)", r.text)
    
    print(match[0])
    if(not match):
        print("Bad Fishe")
    else:
        lower_md5 = match[0][0]
        upper_md5 = match[0][1]
    
    return {lower_md5, upper_md5}

def getCookie2():
    r = requests.get('https://www.cleverbot.com/')
    cookie = r.headers['set-cookie']

    print(cookie)

    return cookie

def encode(msg):
    f = ""
    d = ""
    msg = msg.replace("/[|]/g", "{*}")

    for i in msg:
        if(ord(i) > 255):
            d = repr(i)
            if(d[0:2] == '%u'):
                f += '|' + d[2:]
            else:
                f += d
        else:
            f += i
        
    f = f.replace('|201C', "'").replace('|201D', "'").replace('|2018', "'").replace('|2019', "'").replace('`', "'").replace('%B4', "'").replace('|FF20', '').replace('|FE6B', '')

    print(f)
    return f

async def send(msg):
    body = "stimulus=" + encode(msg)
    # for i in range(0, len(msg)):
    #     body += '&vText' + (i + 2) + '=' + encodeForSending(this.messages[i]);
    body += '&cb_settings_language=en'
    body += '&cb_settings_scripting=no'
    # if (this.internalId):
    #     body += '&sessionid=' + this.internalId

    body += '&islearning=1'
    body += '&icognoid=wsf'
    body += '&icognocheck=' + str(hashlib.md5(body[7:33].encode('utf-8')).hexdigest())

    print(body)

    head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0",
            "Referer": "https://www.cleverbot.com",
            "Origin":  "https://www.cleverbot.com",
            "Cookie": "XVIS=TEI939AFFIAGAYQZ"}
    r = requests.post(url = URL, data = body, timeout = 5000, headers = head)

    print(urllib.parse.unquote(r.headers['CBOUTPUT']))
