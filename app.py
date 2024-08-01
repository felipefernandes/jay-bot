"""
Modulo Flask para tratar e processar os webhooks
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask, request, render_template, jsonify
from main import check_team_wip, sheet_notification_update

app = Flask(__name__)


@app.route('/meeting_post', methods=['POST'])
def meeting_post():
    """Função para tratar o webhook de postagem de notificacao de reunião"""
    return
# TODO: Implementar tratamento do webhook


@app.route('/wipcheck', methods=['POST'])
def wip_check():
    """Mensagens sobre estouro do WIP no Slack"""
    data = request.get_json()

    if not data or 'team_id' not in data:
        return jsonify({"error": "Dados JSON inválidos ou 'team_id' não encontrado"}), 400

    team_id = data['team_id']
    check_team_wip(team_id)
    return jsonify({"message": "Webhook processado"}), 200


@app.route('/sheet-update', methods=['POST'])
def sheet_update():
    """Mensagens sobre atualização de google Sheets no Slack"""
    data = request.get_json()

    if not data or 'team_id' not in data or 'sheet_name' not in data or 'num_rows_updated' not in data:
        return jsonify({"error": "Dados JSON inválidos ou não encontrados"}), 400

    team_id = data['team_id']
    sheet_name = data['sheet_name']
    num_rows_updated = data['num_rows_updated']

    sheet_notification_update(team_id, sheet_name, num_rows_updated)
    return jsonify({"message": "Webhook processado"}), 200

# Homepage aplicação


@app.route('/', methods=['GET'])
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
