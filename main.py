"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
import json
import random
from slack_sdk import WebClient
from config import BOT_USER_OAUTH_TOKEN, JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL
from jira_client import get_jira_client, check_wip_limit
from slack_client import send_slack_message


def check_teams_wip():
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

    # Configurar clientes
    slack_client = WebClient(token=BOT_USER_OAUTH_TOKEN)
    jira_client = get_jira_client(
        JIRA_API_TOKEN, JIRA_SERVER_URL, JIRA_USER_EMAIL)

    # Verificar WIP para cada equipe e enviar alertas
    for team, config in teams_config.items():
        if check_wip_limit(jira_client, config['board_id'], config['wip_limit'], config['states']):
            # Escolher uma mensagem aleatória
            message = random.choice(wip_messages).format(
                team=config['team_name'])
            send_slack_message(slack_client, config['channel'], message)
