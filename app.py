"""
Modulo Flask para tratar e processar os webhooks
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask, request
from main import check_team_wip

app = Flask(__name__)


@app.route('/wipcheck', methods=['POST'])
def webhook():
    # Extrair o team_id do cabeçalho da requisição
    team_id = request.headers.get('team_id')

    if not team_id:
        return "Header 'team_id' não encontrado", 400

    # Chamar a função de verificação passando o team_id
    check_team_wip(team_id)
    return "Webhook processado", 200


if __name__ == "__main__":
    app.run(debug=True)
