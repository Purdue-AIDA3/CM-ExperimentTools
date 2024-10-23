import requests
import json
from datetime import datetime
import time
from pathlib import Path
import os
survey_ids = ["SV_0qdc3A6fsdViGR8", "SV_0kP9iQpsp33Y4lg"]
qualtrics_api_token = "QocORRmAwUvVPs45TN75dAC1CwRdegXc5ciAWE8l"
survey_names = ["Intake Survey", "NASA-TLX"]
base_url = "https://purdue.ca1.qualtrics.com/API/v3/surveys"
def start_export(survey_id):
    headers = {
        "X-API-TOKEN": qualtrics_api_token,
        "Content-Type": "application/json"
    }
    response = requests.post(f'{base_url}/{survey_id}/export-responses', headers=headers, json={'format':'json', 'compress': 'false'})
    if response.status_code == 200:
        return response.json()["result"]["progressId"]
    else:
        print("Failed to start export request:", response.text)
        return None

def wait_for_response(survey_id, progress_id):
    while True:
        headers = {
            "X-API-TOKEN": qualtrics_api_token,
            "Content-Type": "application/json"
        }
        response = requests.get(f'{base_url}/{survey_id}/export-responses/{progress_id}', headers=headers)
        if response.status_code == 200:
            resoinse = response.json()
            if response.json()["result"]["status"] == 'complete':
                return response.json()["result"]["fileId"]
            else:
                time.sleep(3)
        else:
            print("Failed to check for responses:", response.text)
            return None

def get_responses(survey_id, file_id):
    while True:
        headers = {
            "X-API-TOKEN": qualtrics_api_token,
            "Content-Type": "application/json"
        }
        response = requests.get(f'{base_url}/{survey_id}/export-responses/{file_id}/file', headers=headers)
        if response.status_code == 200:
            return response.json()['responses']
        else:
            print("Failed to export survey responses:", response.text)
            return None
def fetch_survey_responses(survey_id):
    progress_id = start_export(survey_id)
    if progress_id == None:
        return None
    file_id = wait_for_response(survey_id, progress_id)
    if file_id == None:
        return None
    return get_responses(survey_id, file_id)
    
def save_responses(survey_name, responses):
    for response in responses:
        uid = response["values"].get("userid", None)
        directory = f"\\\\datadepot.rcac.purdue.edu\\depot\\sbrunswi\\data\\{uid}"
        if uid == None or not os.path.isdir(directory):
            print(f"Skipping {uid}, directory does not exist")
            continue
        directory += "\\surveys_responses"
        Path(directory).mkdir(exist_ok=True)
        task_id = response["values"].get("taskid", None)
        if task_id != None:
            file_name = f"{directory}\\{survey_name}_{task_id}.json"
        else:
            file_name = f"{directory}\\{survey_name}.json"
        with open(file_name, 'w') as f:
            json.dump(response, f, indent=4)

if __name__ == "__main__":
    for survey_id, survey_name in zip(survey_ids, survey_names):
        responses = fetch_survey_responses(survey_id)
        if responses:
            save_responses(survey_name, responses)
