#!/usr/bin/env python3
'''
'''
import json
import base64
from google.cloud import secretmanager
import requests
PROJECT_ID = "{PROJECT_ID}"
SECRET_ID = "{SECRET_ID}"


########################################################################################
# Initial function to parse the message
########################################################################################
def run_notifier(event, context):  
    try:
        data = base64.b64decode(event['data']).decode('utf-8')
        try:
            data_json = json.loads(data.strip())
        except:
            data_json = data

        print("Got {}".format(data_json))

        # Parse fields, some don't always exist
        log_url             = data_json['logUrl']
        status              = data_json['status']
        try:
            build_trigger_id    = data_json['buildTriggerId']
        except:
            build_trigger_id    = "None"
        try:
            repo_name           = data_json['source']['repoSource']['repoName']
        except:
            print("No repo name found.  Exiting")
            return
        try:
            commit_sha          = data_json['source']['repoSource']['commitSha']
        except:
            commit_sha          = ""
            print("No sha found")
            if status != "FAILURE":
                print("Exiting")
                return
        try:
            short_sha           = data_json['substitutions']['SHORT_SHA']
        except:
            short_sha           = ""
            print("No short sha found")
            if status != "FAILURE":
                print("Exiting")
                return

        # Exit if not failed nor success
        if status not in ("SUCCESS", "FAILURE", "TIMEOUT"):
            print("Skipping...not a success, fail, or timeout")
            return

        # Make the initial message
        if status == "SUCCESS":
            text    = "{} build succeeded".format(repo_name)
            color   =  "#1a8f35"
        elif status == "FAILURE":
            text    = '''{} build FAILED
{}
'''.format(repo_name, get_failure_step(data_json=data_json))
            color   =  "#cc361f"
        elif status == "TIMEOUT":
            text    = '''{} build TIMEDOUT
{}
'''.format(repo_name, get_failure_step(data_json=data_json))
            color   =  "#cc361f"

        # Build the slack post
        attachments=[
            {
                "text": text,
                "color": color,
                "actions": [
                    {
                        "name": "action",
                        "type": "button",
                        "text": "Cloud Build Logs",
                        "url": log_url
                    },
                ],
            }
        ]

        # Send the slack notification
        send_slack_notification(attachments=attachments)
    except Exception as e:
        print("Error: {}".format(str(e)))


def send_slack_notification(attachments):
    webhook_url = get_secret_manager_secret(PROJECT_ID=PROJECT_ID, SECRET_ID=SECRET_ID)
    json_data = {"attachments" : attachments, "username":"cloud-build-status"}
    requests.post(webhook_url, data=json.dumps(json_data), verify=False, headers={'Content-Type': 'application/json'})


def get_secret_manager_secret(PROJECT_ID, SECRET_ID):
    try:
        # Import the Secret Manager client library.
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        # Get the secret
        request = {"name": "projects/{}/secrets/{}/versions/latest".format(PROJECT_ID, SECRET_ID)}
        response = client.access_secret_version(request)
        secret_string = response.payload.data.decode("UTF-8")
        try:
            return json.loads(secret_string)
        except:
            return secret_string
    except Exception as e:
        print("Error getting json creds: %s" % (str(e)))
        return {}


def get_failure_step(data_json):
    try:
        for num, step in enumerate(data_json['steps']):
            if step['status'] != "SUCCESS":
                return '''Step #{}: 
    Command: {}
    Arguments: {}
    '''.format(num, step['name'], step['args'])

        return None
    except:
        return "Failure before any steps occured"
