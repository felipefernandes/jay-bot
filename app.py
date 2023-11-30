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
    data = request.json
    team_id = data.get("team_id")  # Assumindo que o JIRA envia o ID do time
    if team_id:
        check_team_wip(team_id)
    return "Webhook processado", 200


if __name__ == "__main__":
    app.run(debug=True)
