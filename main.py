"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import json
import random
from slack_sdk import WebClient
from config import BOT_USER_OAUTH_TOKEN, JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL
from jira_client import get_jira_client, check_wip_limit
from slack_client import send_slack_message


def check_team_wip(team_id):
    # Carregar configurações das equipes
    try:
        with open('teams_config.json', encoding='utf-8') as f:
            teams_config = json.load(f)
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado.")
        exit(1)

    # Carregar mensagens de WIP
    try:
        with open('wip_messages.json', encoding='utf-8') as f:
            wip_messages = json.load(f)["messages"]
    except FileNotFoundError:
        print("Arquivo de mensagens WIP não encontrado.")
        exit(1)

    team_config = teams_config.get(team_id)
    if not team_config:
        print(f"Configuração não encontrada para o time: {team_id}")
        return

    # Configurar clientes
    slack_client = WebClient(token=BOT_USER_OAUTH_TOKEN)
    jira_client = get_jira_client(
        JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL)

    # Preparar argumentos para a função check_wip_limit
    board_id = team_config['board_id']
    wip_limit = team_config['wip_limit']
    states = team_config['states']

    # Verificar WIP para o time específico e enviar alerta
    if check_wip_limit(jira_client, board_id, wip_limit, states):
        # Escolher uma mensagem aleatória
        message = random.choice(wip_messages).format(team=team_config['team_name'])
        send_slack_message(slack_client, team_config['channel'], message)
