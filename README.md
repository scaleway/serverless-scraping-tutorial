# Create a serverless scraping architecture

This is the code for the tutorial [Create a serverless scraping architecture, with Scaleway Messaging and Queuing SQS, Serverless Functions and Managed Database](https://www.scaleway.com/en/docs/tutorials/create-serverless-scraping).

In this tutorial we show how to set up a simple application which reads [Hacker News](https://news.ycombinator.com/news) and processes the articles it finds there asynchronously. To do so, we use Scaleway serverless products and deploy two functions:
- A producer function, activated by a recurrent cron trigger, that scrapes HackerNews for articles published in the last 15 minutes and pushes the title and URL of the articles to an SQS queue created with Scaleway Messaging and Queuing.
- A consumer function, triggered by each new message on the SQS queue, that consumes messages published to the queue, scrapes some data from the linked article, and then writes the data into a Scaleway Managed Database.

## Requirements

This example assumes you are familiar with how serverless functions work. If needed, you can
check [Scaleway official documentation](https://www.scaleway.com/en/docs/serverless/functions/quickstart/)

You will also need Python and Terraform.


## Running

```bash
cd scraper
pip install -r requirements.txt --target ./package
zip -r functions.zip handlers/ package/
cd ../consumer
pip install -r requirements.txt --target ./package
zip -r functions.zip handlers/ package/
cd ../terraform 
terraform init
terraform apply
```
