# On-Call Notifier
This project fetches on-call information from PagerDuty and sends a message to a specified Slack channel. It uses GitHub Actions to automate this process on a schedule.
## Prerequisites

**PagerDuty API Token**: You need a PagerDuty API token to access PagerDuty's API.
**Slack Bot Token**: You need a Slack Bot token to send messages to a Slack channel.
**Primary and Secondary Schedule IDs**: You need the IDs of the primary and secondary PagerDuty schedules.

## Setup
### Environment Variables
Create a `.env` file in the root directory of your project and add the following variables:
```env
PAGERDUTY_API_TOKEN=your_pagerduty_api_token
SLACK_BOT_TOKEN=your_slack_bot_token
