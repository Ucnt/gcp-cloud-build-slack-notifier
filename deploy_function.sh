#!/bin/bash

gcloud functions deploy cloud-build-notifier \
  --project=$1 \
  --memory=256MB \
  --runtime=python37 \
  --trigger-topic=cloud-builds \
  --source=./source \
  --entry-point=run_notifier \
  --service-account=$2