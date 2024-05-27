"""
Modulo de interacao com Slack
"""
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def send_message(self, channel, message):
        """
        Envia uma mensagem para um canal específico no Slack.

        :param channel: O canal para enviar a mensagem.
        :param message: A mensagem a ser enviada.
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel, text=message)
            if not response.get("ok"):
                print(f"Erro ao enviar mensagem: {response.get('error')}")
        except SlackApiError as e:
            print(f"Erro na API do Slack: {e.response['error']}")
