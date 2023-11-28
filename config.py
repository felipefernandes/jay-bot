"""
Modulo de configuracao
"""
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
SLACK_API_TOKEN = os.getenv("SLACK_TOKEN")
BOT_USER_OAUTH_TOKEN = os.getenv("BOT_OAUTH_TOKEN")
JIRA_SERVER_URL = os.getenv("JIRA_SERVER_URL")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")
