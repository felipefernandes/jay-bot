"""
Módulo Flask para tratar e processar os webhooks.
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import logging
from flask import Flask, request, render_template, jsonify
from progress_tracker import check_progress_status
from main import check_team_wip, sheet_notification_update

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/check_progress_status', methods=['POST'])
def progress_status_check():
    """
    Endpoint para verificar o progresso de um épico e enviar mensagem no Slack.
    """
    data = request.get_json()

    if not data or 'team_id' not in data or 'epic_id' not in data or 'label' not in data:
        logger.error("Dados JSON inválidos ou campos ausentes: %s", data)
        return jsonify({"error": "Dados JSON inválidos ou campos ausentes"}), 400

    team_id = data["team_id"]
    epic_id = data['epic_id']
    label = data['label']

    try:
        check_progress_status(team_id, epic_id, label)
    except Exception as e:
        logger.error("Erro ao verificar progresso: %s", e)
        return jsonify({"error": "Erro ao processar webhook"}), 500

    return jsonify({"message": "Webhook processado"}), 200

@app.route('/wipcheck', methods=['POST'])
def wip_check():
    """
    Endpoint para verificar estouro de WIP e alertar no Slack.
    """
    data = request.get_json()

    if not data or 'team_id' not in data:
        logger.error("Dados JSON inválidos ou 'team_id' não encontrado: %s", data)
        return jsonify({"error": "Dados JSON inválidos ou 'team_id' não encontrado"}), 400

    team_id = data['team_id']

    try:
        check_team_wip(team_id)
    except Exception as e:
        logger.error("Erro ao verificar WIP: %s", e)
        return jsonify({"error": "Erro ao processar webhook"}), 500

    return jsonify({"message": "Webhook processado"}), 200

@app.route('/sheet-update', methods=['POST'])
def sheet_update():
    """
    Endpoint para receber notificações de alteração em uma planilha do Google Sheets.
    """
    data = request.get_json()

    if not data or 'team_id' not in data or 'sheet_name' not in data or 'num_rows_updated' not in data:
        logger.error("Dados JSON inválidos ou não encontrados: %s", data)
        return jsonify({"error": "Dados JSON inválidos ou não encontrados"}), 400

    team_id = data['team_id']
    sheet_name = data['sheet_name']
    num_rows_updated = data['num_rows_updated']

    try:
        sheet_notification_update(team_id, sheet_name, num_rows_updated)
    except Exception as e:
        logger.error("Erro ao notificar atualização de planilha: %s", e)
        return jsonify({"error": "Erro ao processar webhook"}), 500

    return jsonify({"message": "Webhook processado"}), 200

@app.route('/', methods=['GET'])
def homepage():
    """
    Página inicial do bot.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
