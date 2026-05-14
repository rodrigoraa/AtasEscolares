from dataclasses import dataclass


@dataclass(frozen=True)
class RegraDisciplina:
    artigo: str
    inciso: str
    gravidade: str
    sancao: str
    orientacao: str


REGRAS_OCORRENCIA: dict[str, RegraDisciplina] = {
    "Uso de celular em sala": RegraDisciplina(
        "82",
        "II",
        "Falta leve",
        "Advertência verbal",
        "Orientar sobre o uso de aparelhos eletrônicos somente quando autorizado para fins pedagógicos.",
    ),
    "Entrada ou saída da sala sem permissão": RegraDisciplina(
        "82",
        "I",
        "Falta leve",
        "Advertência verbal",
        "Reforçar a necessidade de autorização prévia para entrada ou saída da sala.",
    ),
    "Uso de tereré no ambiente escolar": RegraDisciplina(
        "82",
        "III",
        "Falta leve",
        "Advertência verbal",
        "Orientar que trazer ou tomar tereré no ambiente escolar é vedado pelo regimento.",
    ),
    "Uso de objeto de terceiro sem autorização": RegraDisciplina(
        "82",
        "IV",
        "Falta leve",
        "Advertência verbal",
        "Orientar sobre respeito aos pertences de terceiros e necessidade de autorização.",
    ),
    "Fumo ou cigarro eletrônico": RegraDisciplina(
        "82",
        "V",
        "Falta moderada",
        "Repreensão escrita",
        "Alertar sobre a proibição de fumar ou utilizar dispositivos similares no ambiente escolar.",
    ),
    "Ausência da escola ou sala sem autorização": RegraDisciplina(
        "82",
        "VI",
        "Falta moderada",
        "Repreensão escrita",
        "Reforçar a obrigação de permanência no período escolar e saída somente com autorização.",
    ),
    "Desperdício de material da escola": RegraDisciplina(
        "82",
        "VII",
        "Falta moderada",
        "Repreensão escrita",
        "Orientar sobre uso responsável de materiais comuns e preservação dos recursos escolares.",
    ),
    "Presença de pessoa estranha": RegraDisciplina(
        "82",
        "VIII",
        "Falta moderada",
        "Repreensão escrita",
        "Esclarecer que é proibido incentivar ou acompanhar a presença de pessoas estranhas.",
    ),
    "Uniforme irregular": RegraDisciplina(
        "82",
        "IX",
        "Falta moderada",
        "Repreensão escrita",
        "Reforçar o dever de apresentar-se com vestimenta adequada e uniforme conforme orientação escolar.",
    ),
    "Efeito de álcool ou substância": RegraDisciplina(
        "82",
        "X",
        "Falta grave",
        "Ações educativas",
        "Adotar orientação formal e encaminhamentos cabíveis para proteção do estudante e da comunidade escolar.",
    ),
    "Evento sem autorização": RegraDisciplina(
        "82",
        "XI",
        "Falta grave",
        "Ações educativas",
        "Orientar que eventos ou atividades extras dependem de autorização da unidade escolar.",
    ),
    "Algazarra ou incitação contra normas": RegraDisciplina(
        "82",
        "XII",
        "Falta grave",
        "Ações educativas",
        "Trabalhar a responsabilidade coletiva e o respeito às normas regimentais.",
    ),
    "Desacato": RegraDisciplina(
        "82",
        "XIII",
        "Falta grave",
        "Ações educativas",
        "Orientar sobre civilidade, respeito e postura adequada diante dos integrantes da escola.",
    ),
    "Dano ao patrimônio": RegraDisciplina(
        "82",
        "XIV",
        "Falta grave",
        "Ações educativas",
        "Registrar a necessidade de reparação, preservação do patrimônio público e responsabilização cabível.",
    ),
    "Ofensa verbal ou agressão moral": RegraDisciplina(
        "82",
        "XV",
        "Falta grave",
        "Ações educativas",
        "Orientar sobre respeito, convivência pacífica e prevenção de danos morais ou físicos.",
    ),
    "Uso da internet para denegrir imagem": RegraDisciplina(
        "82",
        "XVII",
        "Falta grave",
        "Ações educativas",
        "Alertar sobre responsabilidade no uso da internet e respeito à imagem da comunidade escolar.",
    ),
    "Agressão física": RegraDisciplina(
        "82",
        "XVIII",
        "Falta gravíssima",
        "Suspensão orientada de até 2 dias consecutivos",
        "Adotar providências imediatas de proteção, mediação e comunicação aos responsáveis.",
    ),
    "Falsificação ou rasura de documento": RegraDisciplina(
        "82",
        "XIX",
        "Falta gravíssima",
        "Suspensão orientada de até 2 dias consecutivos",
        "Orientar sobre a gravidade da adulteração documental e registrar os encaminhamentos cabíveis.",
    ),
    "Porte de objeto cortante, arma, explosivo ou objeto perigoso": RegraDisciplina(
        "82",
        "XX",
        "Falta gravíssima",
        "Suspensão orientada de até 2 dias consecutivos",
        "Priorizar a segurança da comunidade escolar e acionar os encaminhamentos institucionais necessários.",
    ),
    "Consumo ou manuseio de drogas": RegraDisciplina(
        "82",
        "XXI",
        "Falta gravíssima",
        "Suspensão orientada de até 2 dias consecutivos",
        "Realizar registro formal, comunicação responsável e encaminhamentos de proteção cabíveis.",
    ),
}


AGRAVAMENTO_REINCIDENCIA = {
    "Falta leve": ("Falta moderada", "Repreensão escrita"),
    "Falta moderada": ("Falta grave", "Ações educativas"),
    "Falta grave": ("Falta gravíssima", "Suspensão orientada de até 2 dias consecutivos"),
    "Falta gravíssima": ("Transferência compulsória", "Transferência compulsória"),
}


def tipos_ocorrencia() -> list[str]:
    return list(REGRAS_OCORRENCIA.keys())


def sugerir_regra(tipo_ocorrencia: str, reincidencia: bool = False) -> RegraDisciplina:
    regra = REGRAS_OCORRENCIA.get(
        tipo_ocorrencia,
        RegraDisciplina(
            "81",
            "VI",
            "Falta leve",
            "Advertência verbal",
            "Orientar o estudante quanto à boa conduta e às normas de convivência escolar.",
        ),
    )

    if reincidencia and regra.gravidade in AGRAVAMENTO_REINCIDENCIA:
        gravidade, sancao = AGRAVAMENTO_REINCIDENCIA[regra.gravidade]
        return RegraDisciplina(
            regra.artigo,
            regra.inciso,
            gravidade,
            sancao,
            f"{regra.orientacao} Considerar a reincidência para acompanhamento pedagógico e disciplinar.",
        )

    return regra
