# Create a serverless scraping architecture, with Scaleway Messaging and Queuing SQS, Serverless Functions and Managed Database

Code for Scaleway serverless scraping tutorial. 

Producer function code is in the `scraper` directory, consumer function in the `consumer` directory, and terraform (you guessed it) in the `terraform` directory.

If you have already set up the terraform provider, you only have to zip the functions and deploy the infrastructure launching the `apply` command.

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