import requests
import urllib3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
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
def get_oncall_user(schedule_id, time_range):
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(weeks=time_range)
    end_time = start_time + timedelta(weeks=1)
    url = f'https://api.pagerduty.com/oncalls?schedule_ids[]={schedule_id}&since={start_time.isoformat()}&until={end_time.isoformat()}'
    headers = {
        'Authorization': f'Token token={PAGERDUTY_API_TOKEN}',
        'Accept': 'application/vnd.pagerduty+json;version=2'
    }
    response = requests.get(url, headers=headers, verify=False)  # Disable SSL verification
    data = response.json()
    print(data)  # Debugging output
    # Find the first on-call user
    for oncall in data['oncalls']:
        if 'user' in oncall and 'summary' in oncall['user']:
            return oncall['user']['summary']
    return None
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
    messages = []
    for i in range(3):
        week_number = i
        primary_oncall_user = get_oncall_user(PRIMARY_SCHEDULE_ID, week_number)
        secondary_oncall_user = get_oncall_user(SECONDARY_SCHEDULE_ID, week_number)
        if primary_oncall_user or secondary_oncall_user:
            current_week = "This week" if week_number == 0 else f"{week_number} weeks out"
            primary_message = f'*{current_week} Primary Incident Manager*: {primary_oncall_user}' if primary_oncall_user else ''
            secondary_message = f'*{current_week} Secondary Incident Manager*: {secondary_oncall_user}' if secondary_oncall_user else ''
            message = f'{primary_message}\n{secondary_message}'
            messages.append(message)
    final_message = '\n\n'.join(messages)
    if final_message:
        response = send_to_slack(final_message)
        print(response)
    else:
        print("No Incident Managers currently on call.")
if __name__ == "__main__":
    main()
