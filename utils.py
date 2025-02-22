import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_file(filename):
    """Carrega um arquivo JSON e retorna seu conteúdo."""
    try:
        with open(filename, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Arquivo de configuração não encontrado: %s", filename)
        exit(1)
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar o arquivo JSON: %s", filename)
        exit(1)
    except Exception as e:
        logger.error("Erro inesperado ao carregar o arquivo JSON %s: %s", filename, e)
        exit(1)

def create_progress_bar(percent, length=20):
    """Gera uma barra de progresso visual baseada no percentual informado."""
    try:
        filled_length = int(length * percent // 100)
        progress_bar = "█" * filled_length + "-" * (length - filled_length)
        return f"[{progress_bar}] {percent:.2f}%"
    except Exception as e:
        logger.error("Erro ao criar a barra de progresso: %s", e)
        return "[Erro ao criar a barra de progresso]"
