import requests
import base64

response = requests.post(url="http://www.sqfgc.com:80/sqfc/publish/lp/getImageVerifyCode.do")
if response.status_code == 200:
    response_json = response.json()
    message = response_json.get("message")
    errorCode = response_json.get("errorCode")
    success = response_json.get("success")
    dataInfo = response_json.get("dataInfo").get("dataInfo")
    capcode = dataInfo.get('capcode')
    smallImage = dataInfo.get('smallImage')
    yHeight = dataInfo.get('yHeight')
    bigImage = dataInfo.get('bigImage')
    bigimage_bytes = base64.b64decode(bigImage)
    small_bytes = base64.b64decode(smallImage)
    with open('./bigimage.jpg', 'wb+') as fp:
        fp.write(bigimage_bytes)
    with open('./smallimage.jpg', 'wb+') as fp:
        fp.write(small_bytes)


