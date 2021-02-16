import os
import requests

# Lineのアクセスコード
URL = "https://notify-api.line.me/api/notify"
ACCESS_TOKEN = ''
HEADERS = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

# Send Message to LINE
def pushLine(url, access_token, headers, line_message):
    payload = {'message': line_message}
    r = requests.post(url, headers=headers, params=payload,)

# Send Picture to LINE
def pushPicture(url, access_token, headers, line_message, image_file):
    payload = {"message": line_message}
    files = {"imageFile": open(image_file, "rb")}
    res = requests.post(url, headers=headers, params=payload, files=files)
