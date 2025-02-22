import openai
import os
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Configurar API OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY não encontrado nas variáveis de ambiente.")
    raise ValueError("OPENAI_API_KEY não encontrado nas variáveis de ambiente.")
openai.api_key = api_key

def gerar_mensagem_motivacional(progresso):
    """
    Gera uma mensagem motivacional baseada no progresso do épico.
    """
    prompt = f"""
    O progresso do épico está em {progresso:.2f}%! Queremos motivar o time com uma mensagem espirituosa, divertida e bem-humorada.
    - Se estiver abaixo de 25%, incentive o time a começar forte.
    - Se estiver entre 25% e 50%, reconheça o progresso e motive a continuidade.
    - Se estiver entre 50% e 75%, mostre que estamos no caminho certo e quase lá.
    - Se estiver entre 75% e 99%, crie uma sensação de "quase lá".
    - Se for 100%, celebre com tudo, como se fosse um treinador vibrando com o time!

    Crie uma mensagem curta, animada, usando emojis e tom bem motivador.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um bot motivacional que fala de forma divertida e animada."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error("Erro ao gerar mensagem motivacional: %s", e)
        return "⚠️ Erro ao gerar mensagem motivacional. Tente novamente mais tarde."
