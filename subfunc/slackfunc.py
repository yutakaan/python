import requests
import json
from subfunc import token
from slack_sdk import WebClient

# Slack WebhookURL
WEBHOOK_URL = token.SLACK_WEBHOOK_URL
HEADERS = {"Content-Type": "application/json"}
TOKEN = token.SLACK_TOKEN
CHANNEL = token.SLACK_CHANNEL

# Send Message to Slack
def postSlackText(webhook_url, headers, title, text):
    data = {
            "attachments":[{
                "fields":[{
                    "title": title,
                    "value": text
                }]
            }]
     }
    json_data = json.dumps(data)
    response = requests.post(webhook_url, data=json_data, headers=headers)

# Send Message with Picture to Slack
def postSlackTextWithPicture(token, channel, title, text, image):
    client = WebClient(token)
    response = client.files_upload_v2(
                    channel=channel,
                    title=title,
                    file=image,
                    initial_comment=text
                )
