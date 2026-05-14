ASSINATURAS_PADRAO = [
    "Direção",
    "Coordenação",
    "Estudante",
    "Responsável",
    "Testemunha",
]


def normalizar_assinaturas(assinaturas: list[str] | None) -> list[str]:
    if not assinaturas:
        return ASSINATURAS_PADRAO.copy()

    permitidas = set(ASSINATURAS_PADRAO)
    escolhidas = []
    for assinatura in assinaturas:
        assinatura = assinatura.strip()
        if assinatura in permitidas and assinatura not in escolhidas:
            escolhidas.append(assinatura)

    return escolhidas or ASSINATURAS_PADRAO.copy()


def serializar_assinaturas(assinaturas: list[str] | None) -> str:
    return "\n".join(normalizar_assinaturas(assinaturas))


def desserializar_assinaturas(valor: str | None) -> list[str]:
    if not valor:
        return ASSINATURAS_PADRAO.copy()
    return normalizar_assinaturas(valor.splitlines())
