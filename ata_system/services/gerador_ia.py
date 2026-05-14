from services.agente_atas import AgenteAtaIndisponivel, agente_atas


class GeracaoIAIndisponivel(AgenteAtaIndisponivel):
    pass


def gerar_ata_com_ia(dados: dict, regra) -> str:
    try:
        return agente_atas.gerar_ata(dados, regra)
    except AgenteAtaIndisponivel as exc:
        raise GeracaoIAIndisponivel(str(exc)) from exc
