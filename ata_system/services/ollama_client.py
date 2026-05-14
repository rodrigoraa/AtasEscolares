import logging
import os
import re
from pathlib import Path

import httpx
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

logger = logging.getLogger(__name__)


class OllamaIndisponivel(RuntimeError):
    pass


PROMPT_SISTEMA = (
    "Você é um assistente administrativo escolar. Reescreva a ata abaixo em linguagem "
    "formal, objetiva e adequada à coordenação pedagógica, sem aumentar o tamanho do texto. "
    "Não invente fatos. "
    "Não altere nome de aluno, data, turma, artigo, inciso, gravidade ou sanção. "
    "Não acrescente punições não previstas. "
    "Não mencione leis ou artigos que não estejam nos dados enviados. "
    "Mantenha o texto em formato de ata escolar. "
    "Não crie cabeçalho, título, lista de dados, campos separados ou linhas de assinatura. "
    "Varie a redação para que o texto não fique repetitivo, mas preserve o sentido. "
    "Evite linguagem acusatória; use linguagem de registro administrativo. "
    "Retorne somente o texto final da ata, sem explicações, comentários ou listas."
)


def ollama_base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.2:3b").strip() or "llama3.2:3b"


def ollama_timeout() -> float:
    try:
        return float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))
    except ValueError:
        return 120.0


def ollama_num_predict() -> int:
    try:
        return int(os.getenv("OLLAMA_NUM_PREDICT", "420"))
    except ValueError:
        return 420


def valor_texto(valor) -> str:
    if valor is None:
        return ""
    texto = str(valor).strip()
    if texto.lower() in {"none", "null", "undefined"}:
        return ""
    return texto


def sim_nao(valor) -> str:
    return "sim" if bool(valor) else "não"


def montar_prompt_usuario(dados_ata: dict, texto_base: str) -> str:
    return f"""
Dados obrigatórios que não podem ser alterados:
Ata {valor_texto(dados_ata.get("numero"))}/{valor_texto(dados_ata.get("ano"))}; data {valor_texto(dados_ata.get("data_ocorrencia"))}; período {valor_texto(dados_ata.get("periodo"))}; local {valor_texto(dados_ata.get("local"))}; aluno(s) {valor_texto(dados_ata.get("alunos"))}; turma {valor_texto(dados_ata.get("turma"))}; Art. {valor_texto(dados_ata.get("artigo"))}, inciso {valor_texto(dados_ata.get("inciso"))}; {valor_texto(dados_ata.get("gravidade"))}; {valor_texto(dados_ata.get("sancao"))}.

Texto base para revisar:
{texto_base}

Reescreva apenas o texto base em parágrafos corridos. Preserve os dados obrigatórios. Não aumente a extensão. Não copie a lista de dados obrigatórios para a resposta.
""".strip()


def resposta_parece_recusa(texto: str) -> bool:
    texto_normalizado = texto.lower()
    recusas = [
        "não posso fornecer",
        "nao posso fornecer",
        "não posso ajudar",
        "nao posso ajudar",
        "não posso criar",
        "nao posso criar",
        "posso ajudar com outra coisa",
        "não tenho permissão",
        "nao tenho permissao",
    ]
    return any(recusa in texto_normalizado for recusa in recusas)


def validar_resposta(texto: str, dados_ata: dict) -> str:
    texto = texto.strip()
    if not texto:
        raise OllamaIndisponivel("Ollama retornou texto vazio.")
    if resposta_parece_recusa(texto):
        raise OllamaIndisponivel("Ollama recusou a reescrita da ata.")
    if resposta_parece_cortada(texto):
        raise OllamaIndisponivel("Ollama retornou texto incompleto.")

    artigo = valor_texto(dados_ata.get("artigo"))
    inciso = valor_texto(dados_ata.get("inciso"))
    if artigo and not re.search(rf"\b(art\.?|artigo)\s*{re.escape(artigo)}\b", texto, flags=re.IGNORECASE):
        raise OllamaIndisponivel("Ollama não preservou o artigo definido pelo sistema.")
    if inciso and not re.search(rf"\binciso\s*{re.escape(inciso)}\b", texto, flags=re.IGNORECASE):
        raise OllamaIndisponivel("Ollama não preservou o inciso definido pelo sistema.")

    return texto


def resposta_parece_cortada(texto: str) -> bool:
    final = texto.rstrip()
    if not final:
        return True
    if final[-1] not in ".!?":
        return True
    ultima_palavra = final.split()[-1].strip(".,;:!?").lower()
    return ultima_palavra in {
        "a",
        "à",
        "ao",
        "as",
        "às",
        "de",
        "da",
        "do",
        "das",
        "dos",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "para",
        "por",
        "com",
        "e",
        "que",
    }


def gerar_texto_com_ollama(dados_ata: dict, texto_base: str) -> str:
    url = f"{ollama_base_url()}/api/chat"
    payload = {
        "model": ollama_model(),
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": montar_prompt_usuario(dados_ata, texto_base)},
        ],
        "stream": False,
        "options": {
            "temperature": 0.4,
            "top_p": 0.9,
            "num_predict": ollama_num_predict(),
        },
    }

    try:
        response = httpx.post(url, json=payload, timeout=ollama_timeout())
        response.raise_for_status()
        data = response.json()
        texto = data["message"]["content"]
    except httpx.TimeoutException as exc:
        logger.warning("Timeout ao chamar Ollama em %s", url)
        raise OllamaIndisponivel("tempo limite excedido ao chamar a IA local.") from exc
    except httpx.ConnectError as exc:
        logger.warning("Ollama indisponível em %s: %s", url, exc)
        raise OllamaIndisponivel("IA local indisponível.") from exc
    except httpx.HTTPStatusError as exc:
        logger.warning("Erro HTTP do Ollama: %s - %s", exc.response.status_code, exc.response.text)
        raise OllamaIndisponivel(f"IA local retornou erro HTTP {exc.response.status_code}.") from exc
    except (KeyError, ValueError, TypeError) as exc:
        logger.warning("Resposta inesperada do Ollama: %s", exc)
        raise OllamaIndisponivel("IA local retornou resposta inesperada.") from exc
    except httpx.HTTPError as exc:
        logger.warning("Falha ao chamar Ollama em %s: %s", url, exc)
        raise OllamaIndisponivel("falha ao chamar a IA local.") from exc

    return validar_resposta(texto, dados_ata)
