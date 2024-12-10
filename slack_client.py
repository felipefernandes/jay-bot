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

    def send_message(self, channel, message=None, blocks=None, debug=0):
        """
        Envia uma mensagem para um canal específico no Slack.

        :param channel: O canal para enviar a mensagem.
        :param message: Texto simples da mensagem.
        :param blocks: Blocos de mensagem em formato JSON.
        :param debug: Flag para habilitar o modo debug (0 ou 1).
        """
        try:
            # Adiciona modo debug à mensagem ou aos blocos
            if debug == 1:
                debug_message = "⚠️ *Modo DEBUG Ativado*\n"
                if blocks:
                    blocks.insert(0, {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": debug_message
                        }
                    })
                elif message:
                    message = debug_message + message

            # Envia a mensagem, priorizando blocos
            response = self.client.chat_postMessage(
                channel=channel,
                text=message if not blocks else None,
                blocks=blocks
            )

            if not response.get("ok"):
                print(f"Erro ao enviar mensagem: {response.get('error')}")
        except SlackApiError as e:
            print(f"Erro na API do Slack: {e.response['error']}")
