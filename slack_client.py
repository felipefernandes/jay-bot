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
        # Verifique se a resposta contém um status de sucesso
        if not response.get("ok"):
            # Trate o caso em que a resposta não é bem-sucedida
            print(f"Erro ao enviar mensagem: {response.get('error')}")
    except SlackApiError as e:
        # Log ou trate o erro de maneira apropriada
        print(f"Erro na API do Slack: {e.response['error']}")
