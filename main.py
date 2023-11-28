"""
Esse modulo configura e executa um bot SLack que interage com JIRA
"""

import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
SLACK_API_TOKEN = os.getenv("SLACK_TOKEN")
BOT_USER_OAUTH_TOKEN = os.getenv("BOT_OAUTH_TOKEN")

# Token do bot
client = WebClient(token=BOT_USER_OAUTH_TOKEN)

try:
    #Enviar mensagem para um canal
    response = client.chat_postMessage(channel='#transformacao-agil', text='Olár')
    assert response["message"]["text"] == "Olár"
except SlackApiError as e:
    assert e.response["error"]