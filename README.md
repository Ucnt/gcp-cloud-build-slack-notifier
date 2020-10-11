# GCP Cloud Build Slack Notifier

## Purpose
Via a Cloud Function, send a Slack webhook notification when a GCP Cloud Build successfully completes or fails via build-in Cloud Build Pub/Sub notifications.

## Requirements
* Cloud Functions, Secrets Manager, and Cloud Build APIs enabled
* Service account with roles/secretmanager.secretAccessor.
* cloud-builds Pub/Sub topic that Cloud Build is sending Pub/Sub messages to.

## Deploy Cloud Function via bash script
* Run: deploy_function.sh {PROJECT_ID} {SERVICE_ACCOUNT}

## Deploy Cloud Function via Cloud Build trigger
1. Modify the cloudbuild.yaml, putting your project ID in place of {PROJECT_ID} and service account in place of {SERVICE_ACCOUNT}
2. Modify the source/main.py file, putting your project ID in place of {PROJECT_ID} and secret ID in place of {SECRET_ID}
3. Add the code to a repo
4. Create a cloud build trigger for the repo
5. Run the trigger to deploy the cloud function

## Example Slack Notifications
[[/screenshot/example-notifications.png|alt=example-notifications]]

## Troubleshooting
* If the cloud-builds topic is not receiving Pub/Sub messages, disable and re-enable the Cloud Builds API.
