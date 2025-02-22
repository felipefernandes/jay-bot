from utils import load_json_file, create_progress_bar
from motivator import gerar_mensagem_motivacional
from config import get_config
from jira_client import JiraClient
from slack_client import SlackClient
import logging

logger = logging.getLogger(__name__)

def check_progress_status(team_id, epic_id, label):
    """Consulta o progresso do épico no JIRA e envia um relatório para o Slack."""
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

    try:
        # Obter status de progresso e título do épico
        progress_status = jira_client.check_progress_status(epic_id, label)
        epic_summary = jira_client.get_epic_summary(epic_id)
        epic_display = f"{epic_summary} ({epic_id})" if epic_summary else epic_id

        if "error" in progress_status:
            message = f"⚠️ *Erro ao obter status de progresso do épico:*\n{progress_status['error']}"
            slack_client.send_message(channel=team_config['channel'], message=message)
            return

        total_issues = progress_status["total_issues"]
        done_issues = progress_status["done_issues"]
        percent_complete = (done_issues / total_issues) * 100 if total_issues > 0 else 0
        progress_bar = create_progress_bar(percent_complete)

        # Gerar mensagem motivacional
        mensagem_motivacional = gerar_mensagem_motivacional(percent_complete)

        # Enviar para Slack
        message = (
            f"📊 *Progresso do {label}*\n"
            f"🗂️ Épico: {epic_display}\n"
            f"- Total de Tarefas: {total_issues}\n"
            f"- Concluídas: {done_issues} ({percent_complete:.2f}%)\n"
            f"- Progresso: {progress_bar}\n\n"
            f"🎉 {mensagem_motivacional}"
        )
        slack_client.send_message(channel=team_config['channel'], message=message)
    except Exception as e:
        logger.error("Erro ao verificar progresso do épico %s: %s", epic_id, e)
        slack_client.send_message(channel=team_config['channel'], message=f"⚠️ *Erro ao verificar progresso do épico:* {epic_id}")
