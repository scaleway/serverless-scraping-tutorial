import boto3
import json 
import os
import psycopg2
import requests
from bs4 import BeautifulSoup

SCW_SQS_URL = "https://sqs.mnq.fr-par.scaleway.com"
queue_url = os.getenv('QUEUE_URL') 
sqs_access_key = os.getenv('SQS_ACCESS_KEY')
sqs_secret_access_key = os.getenv('SQS_SECRET_ACCESS_KEY')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

CREATE_TABLE_IF_NOT_EXISTS = """
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    a_count INTEGER NOT NULL,
    h1_count INTEGER NOT NULL, 
    p_count INTEGER NOT NULL
);"""

INSERT_INTO_ARTICLES = """
INSERT INTO articles (title, url, a_count, h1_count, p_count)
VALUES(%s, %s, %s, %s, %s) RETURNING id
;"""

def scrape_page_for_stats(url):
    page = requests.get(url)
    html_doc = page.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    tags = ['a', 'h1', 'p']

    return {tag: len(soup.find_all(tag)) for tag in tags}

def handle(event, context):
    sqs = boto3.client('sqs', endpoint_url=SCW_SQS_URL, aws_access_key_id=sqs_access_key, aws_secret_access_key=sqs_secret_access_key, region_name='fr-par')

    response = sqs.receive_message(QueueUrl=queue_url, MessageAttributeNames=['All'])
    message_str = response['Messages'][0]
    message = json.loads(message_str)
    message = {'title': 'test', 'url':'http://google.com'}

    tags_count = scrape_page_for_stats(message['url'])
    conn = None
    try: 
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Where else could we create the table?
        cur.execute(CREATE_TABLE_IF_NOT_EXISTS)
        cur.execute(INSERT_INTO_ARTICLES, (message['title'], message['url'], tags_count['a'], tags_count['h1'], tags_count['p']))
        cur.fetchone()[0]
        
        conn.commit()

        cur.close()
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
    except (Exception,psycopg2.DatabaseError) as error:
        return {'statusCode': 500, 'headers': {'content': 'text/plain'}, 'body': {'message': 'error connecting to the db'}}
    finally:
        if conn is not None:
            conn.close()
    return {'statusCode': page.status_code, 'headers': {'content': 'text/plain'}}

if __name__ == '__main__':
    handle(None, None)