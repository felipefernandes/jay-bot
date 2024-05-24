"""
Modulo Flask para tratar e processar os webhooks
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask, request, jsonify
from main import check_team_wip, sheet_notification_update

app = Flask(__name__)


@app.route('/wipcheck', methods=['POST'])
def wip_check():
    # Extrair dados JSON do corpo da requisição
    data = request.get_json()

    # Verificar se os dados JSON foram recebidos corretamente
    if not data or 'team_id' not in data:
        return jsonify({"error": "Dados JSON inválidos ou 'team_id' não encontrado"}), 400

    team_id = data['team_id']

    # Chamar a função de verificação passando o team_id
    check_team_wip(team_id)
    return jsonify({"message": "Webhook processado"}), 200


@app.route('/sheet-update', methods=['POST'])
def sheet_update():
    # Extrair dados JSON do corpo da requisicao
    data = request.get_json()

    # Verificacao se os dados JSON foram recebidos corretamente
    if not data or 'team_id' not in data or 'sheet_name' not in data or 'num_rows_updated' not in data:
        return jsonify({"error": "Dados JSON inválidos ou não encontrados"}), 400

    team_id = data['team_id']
    sheet_name = data['sheet_name']
    num_rows_updated = data['num_rows_updated']

    # Processando e enviando mensagens para o Slack
    sheet_notification_update(
        team_id, sheet_name, num_rows_updated)
    return jsonify({"message": "Webhook processado"}), 200


if __name__ == "__main__":
    app.run(debug=True)
