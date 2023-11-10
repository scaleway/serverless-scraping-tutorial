terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
}

resource "scaleway_account_project" "mnq_tutorial" {
  name = "mnq-tutorial"
}

resource "scaleway_mnq_sqs" "main" {
  project_id = scaleway_account_project.mnq_tutorial.id
}


resource "scaleway_mnq_sqs_credentials" "main_creds" {
  project_id = scaleway_mnq_sqs.main.project_id
  name = "sqs-credentials-main"

  permissions {
    can_manage = true
    can_receive = true
    can_publish = true
  }
}
resource "scaleway_mnq_sqs_credentials" "producer_creds" {
  project_id = scaleway_mnq_sqs.main.project_id
  name = "sqs-credentials-producer"

  permissions {
    can_manage = false
    can_receive = false
    can_publish = true
  }
}

resource "scaleway_mnq_sqs_credentials" "consumer_creds" {
  project_id = scaleway_mnq_sqs.main.project_id
  name = "sqs-credentials-consumer"

  permissions {
    can_manage = false
    can_receive = true
    can_publish = false
  }
}

resource scaleway_mnq_sqs_queue main {
  project_id = scaleway_account_project.mnq_tutorial.id
  name = "hn-queue"
  endpoint = scaleway_mnq_sqs.main.endpoint
  access_key = scaleway_mnq_sqs_credentials.main_creds.access_key
  secret_key = scaleway_mnq_sqs_credentials.main_creds.secret_key
}

resource "scaleway_function_namespace" "mnq_tutorial_namespace" {
  project_id = scaleway_account_project.mnq_tutorial.id
  name        = "mnq-tutorial-namespace"
  description = "Main function namespace"
}

resource scaleway_function scraper {
  namespace_id = scaleway_function_namespace.mnq_tutorial_namespace.id
  project_id = scaleway_account_project.mnq_tutorial.id
  name         = "mnq-hn-scraper"
  runtime      = "python311"
  handler      = "handlers/scrape_hn.handle"
  privacy      = "private"
  timeout      = 10
  zip_file     = "../scraper/functions.zip"
  zip_hash     = filesha256("../scraper/functions.zip")
  deploy       = true
  environment_variables = {
    QUEUE_URL = scaleway_mnq_sqs_queue.main.url
    SQS_ACCESS_KEY = scaleway_mnq_sqs_credentials.producer_creds.access_key
  }
  secret_environment_variables = {
    SQS_SECRET_ACCESS_KEY = scaleway_mnq_sqs_credentials.producer_creds.secret_key
  }
}