"""
Modulo Flask para tratar e processar os webhooks
"""
from flask import Flask
from main import check_teams_wip

app = Flask(__name__)


@app.route('/wipcheck', methods=['POST'])
def webhook():
    """
    # Aqui você pode processar os dados recebidos do JIRA se necessário
    """
    check_teams_wip()  # Esta função deve ser ajustada no main.py
    return "Webhook recebido", 200


if __name__ == "__main__":
    app.run(debug=True)
