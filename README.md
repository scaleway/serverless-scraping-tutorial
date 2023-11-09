# Idea

In this tutorial we are going to cover how to set up a simple scraper for hacker news, asynchronously saving news data on a db, managing service communication via SQS.

1. Scrape HackerNews for news and push title and link to SQS
2a. Trigger a function that saves info on db
 OR
2b. Scrape the website, and either process the text, either save it on s3

SCRAPER -> SQS -> WORKER -> DB