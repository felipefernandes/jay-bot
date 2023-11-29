"""
Modulo de interacao com Slack
"""
from slack_sdk.errors import SlackApiError


def send_slack_message(client, channel, message):
    """
    Envia uma mensagem para um canal específico no Slack.

    :param client: Cliente Slack configurado.
    :param channel: O canal para enviar a mensagem.
    :param message: A mensagem a ser enviada.
    """
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        assert e.response["error"]
