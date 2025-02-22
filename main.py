"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import logging
import random
from progress_tracker import check_progress_status
from utils import load_json_file
from config import get_config
from slack_client import SlackClient
from jira_client import JiraClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_team_wip(team_id):
    """
    Verifica se o time estourou o limite de WIP e envia um alerta no Slack.
    """
    config = get_config()
    teams_config = load_json_file('teams_config.json')
    wip_messages = load_json_file('wip_messages.json').get("messages", [])

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error("Configuração não encontrada para o time: %s", team_id)
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
        message = random.choice(wip_messages).format(team=team_config['team_name'])
        slack_client.send_message(team_config['channel'], message)

def sheet_notification_update(team_id, sheet_name, num_rows_updated):
    """
    Notifica o Slack sobre alterações em uma planilha do Google Sheets.
    """
    config = get_config()
    teams_config = load_json_file('teams_config.json')

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error("Configuração não encontrada para o time: %s", team_id)
        return

    slack_client = SlackClient(config['bot_user_oauth_token'])

    message = f"📝 Foram alteradas {num_rows_updated} linhas na planilha '{sheet_name}' esta semana."
    slack_client.send_message(team_config['channel'], message)

#if __name__ == "__main__":
    # Exemplo de uso local para testar progressos
    # team_id = "team123"
    # epic_id = "BURACO-5336"
    # label = "jornada_real_onboarding"

    # check_progress_status(team_id, epic_id, label)
