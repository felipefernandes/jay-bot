"""
Esse módulo configura e executa um bot Slack que interage com JIRA.
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
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
        logger.error("Arquivo de configuração não encontrado: %s", filename)
        exit(1)


def create_progress_bar(percent, length=20):
    """
    Cria uma barra de progresso visual.

    :param percent: Percentual de progresso (0-100).
    :param length: Comprimento total da barra.
    :return: Uma string representando a barra de progresso.
    """
    filled_length = int(length * percent // 100)
    progress_bar = "█" * filled_length + "-" * (length - filled_length)
    return f"[{progress_bar}] {percent:.2f}%"


def check_progress_status(team_id, epic_id, label):
    config = get_config()
    teams_config = load_json_file('teams_config.json')

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

    # Obter status de progresso e título do épico
    progress_status = jira_client.check_progress_status(epic_id, label)
    epic_summary = jira_client.get_epic_summary(epic_id)
    epic_display = f"{epic_summary} ({epic_id})" if epic_summary else epic_id

    if "error" in progress_status:
        message = f"⚠️ *Erro ao obter status de progresso do marco:*\n{progress_status['error']}"
        slack_client.send_message(
            channel=team_config['channel'], message=message)
        return

    total_issues = progress_status["total_issues"]
    done_issues = progress_status["done_issues"]
    percent_complete = (done_issues / total_issues) * \
        100 if total_issues > 0 else 0
    progress_bar = create_progress_bar(percent_complete)

    # Decide entre usar blocos ou mensagem simples
    use_blocks = False  # Alterne para False se preferir mensagens simples

    if use_blocks:
        # Cria os blocos da mensagem
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📊 Progresso do {label}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Épico*: {epic_display}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"• Total de Tarefas: {total_issues}\n• Concluídas: {done_issues} ({percent_complete:.2f}%)"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Progresso: {progress_bar}"
                }
            }
        ]
        slack_client.send_message(
            channel=team_config['channel'], blocks=blocks)
    else:
        # Envia a mensagem simples
        message = (
            f"📊 *Progresso do {label}*\n"
            f"🗂️ Épico: {epic_display}\n"
            f"- Total de Tarefas: {total_issues}\n"
            f"- Concluídas: {done_issues} ({percent_complete:.2f}%)\n"
            f"- Progresso: {progress_bar}"
        )
        slack_client.send_message(
            channel=team_config['channel'], message=message)


def check_team_wip(team_id):
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
        message = random.choice(wip_messages).format(
            team=team_config['team_name'])
        slack_client.send_message(team_config['channel'], message)


def sheet_notification_update(team_id, sheet_name, num_rows_updated):
    config = get_config()
    teams_config = load_json_file('teams_config.json')

    team_config = teams_config.get(team_id)
    if not team_config:
        logger.error("Configuração não encontrada para o time: %s", team_id)
        return

    slack_client = SlackClient(config['bot_user_oauth_token'])

    message = f"Foram alteradas {num_rows_updated} linhas na planilha '{sheet_name}' esta semana."
    slack_client.send_message(team_config['channel'], message)
