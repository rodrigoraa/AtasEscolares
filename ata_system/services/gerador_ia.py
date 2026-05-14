from services.ollama_client import OllamaIndisponivel, gerar_texto_com_ollama


class GeracaoIAIndisponivel(OllamaIndisponivel):
    pass


def gerar_ata_com_ia(dados: dict, regra, texto_base: str | None = None) -> str:
    dados_ata = {
        **dados,
        "artigo": regra.artigo,
        "inciso": regra.inciso,
        "gravidade": regra.gravidade,
        "sancao": regra.sancao,
    }
    try:
        return gerar_texto_com_ollama(dados_ata, texto_base or "")
    except OllamaIndisponivel as exc:
        raise GeracaoIAIndisponivel(str(exc)) from exc
    except Exception as exc:
        raise GeracaoIAIndisponivel(f"erro inesperado na IA local ({exc}).") from exc
