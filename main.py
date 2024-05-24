"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
import json
import random
import logging
from slack_sdk import WebClient
from config import BOT_USER_OAUTH_TOKEN, JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL
from jira_client import get_jira_client, check_wip_limit
from slack_client import send_slack_message

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o cliente Slack
slack_client = WebClient(token=BOT_USER_OAUTH_TOKEN)


def load_json_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração não encontrado: {filename}")
        exit(1)


def check_team_wip(team_id):
    # Carregar configurações das equipes
    teams_config = load_json_file('teams_config.json')

    # Carregar mensagens de WIP
    wip_messages = load_json_file('wip_messages.json').get("messages", [])

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error(f"Configuração não encontrada para o time: {team_id}")
        return

    # Configurar cliente JIRA
    jira_client = get_jira_client(
        JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL)

    # Preparar argumentos para a função check_wip_limit
    board_id = team_config['board_id']
    wip_limit = team_config['wip_limit']
    states = team_config['states']

    # Verificar WIP para o time específico e enviar alerta
    if check_wip_limit(jira_client, board_id, wip_limit, states):
        # Escolher uma mensagem aleatória
        message = random.choice(wip_messages).format(
            team=team_config['team_name'])
        send_slack_message(slack_client, team_config['channel'], message)


def sheet_notification_update(team_id, sheet_name, num_rows_updated):
    # Carregar configurações das equipes
    teams_config = load_json_file('teams_config.json')

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error(f"Configuração não encontrada para o time: {team_id}")
        return

    # Mensagem para o Slack
    message = (
        f"Foram alteradas {num_rows_updated} linhas na planilha "
        f"'{sheet_name}' esta semana."
    )
    send_slack_message(slack_client, team_config['channel'], message)
