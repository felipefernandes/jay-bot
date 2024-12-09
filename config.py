"""
Modulo de configuracao
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import os

BOT_USER_OAUTH_TOKEN = os.getenv('BOT_USER_OAUTH_TOKEN')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_SERVER_URL = os.getenv('JIRA_SERVER_URL')
JIRA_USER_EMAIL = os.getenv('JIRA_USER_EMAIL')


def get_config():
    return {
        'bot_user_oauth_token': BOT_USER_OAUTH_TOKEN,
        'jira_api_token': JIRA_API_TOKEN,
        'jira_server_url': JIRA_SERVER_URL,
        'jira_user_email': JIRA_USER_EMAIL
    }
