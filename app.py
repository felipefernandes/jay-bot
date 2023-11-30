"""
Modulo Flask para tratar e processar os webhooks
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask, request, jsonify
from main import check_team_wip

app = Flask(__name__)


@app.route('/wipcheck', methods=['POST'])
def webhook():
    # Extrair dados JSON do corpo da requisição
    data = request.get_json()

    # Verificar se os dados JSON foram recebidos corretamente
    if not data or 'team_id' not in data:
        return jsonify({"error": "Dados JSON inválidos ou 'team_id' não encontrado"}), 400

    team_id = data['team_id']

    # Chamar a função de verificação passando o team_id
    check_team_wip(team_id)
    return jsonify({"message": "Webhook processado"}), 200


if __name__ == "__main__":
    app.run(debug=True)
