"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
import json
import random
import logging
from config import get_config
from jira_client import JiraClient
from slack_client import SlackClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_json_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração não encontrado: {filename}")
        exit(1)


def check_team_wip(team_id):
    config = get_config()
    teams_config = load_json_file('teams_config.json')
    wip_messages = load_json_file('wip_messages.json').get("messages", [])

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error(f"Configuração não encontrada para o time: {team_id}")
        return

    slack_client = SlackClient(config['bot_user_oauth_token'])
    jira_client = JiraClient(
        config['jira_api_token'],
        config['jira_server_url'],
        config['jira_user_email']
    )

    board_id = team_config['board_id']
    wip_limit = team_config['wip_limit']
    states = team_config['states']

    if jira_client.check_wip_limit(board_id, wip_limit, states):
        message = random.choice(wip_messages).format(
            team=team_config['team_name'])
        slack_client.send_message(team_config['channel'], message)


def sheet_notification_update(team_id, sheet_name, num_rows_updated):
    config = get_config()
    teams_config = load_json_file('teams_config.json')

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error(f"Configuração não encontrada para o time: {team_id}")
        return

    slack_client = SlackClient(config['bot_user_oauth_token'])

    message = f"Foram alteradas {num_rows_updated} linhas na planilha '{
        sheet_name}' esta semana."
    slack_client.send_message(team_config['channel'], message)
