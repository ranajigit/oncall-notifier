import requests
import urllib3
import os
from dotenv import load_dotenv
# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Load environment variables from .env file
load_dotenv()
# Set your PagerDuty and Slack tokens here
PAGERDUTY_API_TOKEN = os.getenv('PAGERDUTY_API_TOKEN')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL = '#incidents'
PRIMARY_SCHEDULE_ID = 'P2MDXW9'  # Replace with your primary PagerDuty schedule ID
SECONDARY_SCHEDULE_ID = 'PKOXF2X'  # Replace with your secondary PagerDuty schedule ID
# Fetch on-call information from PagerDuty schedule
def get_oncall_user(schedule_id):
    url = f'https://api.pagerduty.com/oncalls?schedule_ids[]={schedule_id}'
    headers = {
        'Authorization': f'Token token={PAGERDUTY_API_TOKEN}',
        'Accept': 'application/vnd.pagerduty+json;version=2'
    }
    response = requests.get(url, headers=headers, verify=False)  # Disable SSL verification
    data = response.json()
    print(data)  # Debugging output
    # Find the correct on-call user
    oncall_user = None
    for oncall in data['oncalls']:
        if 'user' in oncall and 'summary' in oncall['user']:
            oncall_user = oncall['user']['summary']
            break
    return oncall_user
# Send a message to Slack
def send_to_slack(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }
    payload = {
        'channel': SLACK_CHANNEL,
        'text': message
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)  # Disable SSL verification
    return response.json()
def main():
    primary_oncall_user = get_oncall_user(PRIMARY_SCHEDULE_ID)
    secondary_oncall_user = get_oncall_user(SECONDARY_SCHEDULE_ID)
    if primary_oncall_user or secondary_oncall_user:
        messages = []
        if primary_oncall_user:
            messages.append(f'*Primary Incident Manager*: {primary_oncall_user}')
        if secondary_oncall_user:
            messages.append(f'*Secondary Incident Manager*: {secondary_oncall_user}')
        message = '\n'.join(messages)
        response = send_to_slack(message)
        print(response)
    else:
        print("No Incident Manager currently on call.")
if __name__ == "__main__":
    main()