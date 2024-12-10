"""
Modulo de interacao com Slack
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, token=None):
        if not token:
            # Carrega o token do ambiente se não for passado diretamente
            token = os.getenv("BOT_OAUTH_TOKEN")
            if not token:
                raise ValueError(
                    "O token do Slack não foi configurado corretamente.")

        self.client = WebClient(token=token)

    def send_message(self, channel, message, debug=0):
        try:
            if debug == 1:
                message = "⚠️ *Modo DEBUG Ativado*\n" + message

            response = self.client.chat_postMessage(
                channel=channel, text=message)

            if not response.get("ok"):
                print(f"Erro ao enviar mensagem: {response.get('error')}")
        except SlackApiError as e:
            print(f"Erro na API do Slack: {e.response['error']}")
