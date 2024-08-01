from openai import OpenAI
from config import get_config

config = get_config()
OpenAI.api_key = config['openai_api_token']


def generate_message(prompt):
    response = OpenAI.Completions.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=500
    )
    message = response.choices[0].text.strip()
    return message
