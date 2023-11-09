import requests
import boto3
import json 
import os
from bs4 import BeautifulSoup

HN_URL = "https://news.ycombinator.com/newest"
queue_url = os.getenv('QUEUE_URL') 
sqs_access_key = os.getenv('SQS_ACCESS_KEY')
sqs_secret_access_key = os.getenv('SQS_SECRET_ACCESS_KEY')

def handle(event, context):
    page = requests.get(HN_URL)
    html_doc = page.content

    soup = BeautifulSoup(html_doc, 'html.parser')

    titlelines = soup.find_all(class_="titleline")

    sqs = boto3.client('sqs', endpoint_url="https://sqs.mnq.fr-par.scaleway.com", aws_access_key_id=sqs_access_key, aws_secret_access_key=sqs_secret_access_key, region_name='fr-par')

    for titleline in titlelines:
        body_string = json.dumps({'url': titleline.a["href"], 'title': titleline.a.get_text()})
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=body_string)

    return {'statusCode': page.status_code, 'headers': {'content': 'text/plain'}}