"""
Modulo de interacao com Slack
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def send_message(self, channel, message, debug=0):
        """
        Envia uma mensagem para um canal específico no Slack.

        :param channel: O canal para enviar a mensagem.
        :param message: A mensagem a ser enviada.
        """
        try:
            if debug == 1:
                message = "⚠️ *Modo DEBUG Ativado*\n" + message

            response = self.client.chat_postMessage(
                channel=channel, text=message)

            if not response.get("ok"):
                print(f"Erro ao enviar mensagem: {response.get('error')}")
        except SlackApiError as e:
            print(f"Erro na API do Slack: {e.response['error']}")
