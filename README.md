# Cloud Build Slack Notifier

## Purpose
Sends a Slack webhook notification when a GCP Cloud Build successfully comletes or fails via build-in Cloud Build Pub/Sub notifications.

## Requirements
* Service account with roles/secretmanager.secretAccessor.
* cloud-builds Pub/Sub topic that Cloud Build is sending Pub/Sub messages to.

## Execution via Cloud build trigger
1. Modify the cloudbuild.yaml, putting your project ID in place of {PROJECT_ID} and service account in place of {SERVICE_ACCOUNT}
2. Modify the source/main.py file, putting your project ID in place of {PROJECT_ID} and secret ID in place of {SECRET_ID}
3. Add the code to a repo
4. Create a cloud build trigger for the repo
5. Run the trigger to deploy the cloud function

## Slack Notifications
* Successful builds will get a message like this: 

{REPO} build succeeded

* Failed builds will get a message like this:

{REPO} build FAILED
Step #0:
Command: gcr.io/cloud-builders/gcloud
Arguments: [{ARGUMENTS}]

## Troubleshooting
* If the cloud-builds topic is not receiving Pub/Sub messages, disable and re-enable the Cloud Builds API.
