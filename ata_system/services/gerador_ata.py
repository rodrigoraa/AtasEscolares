import random
from datetime import date


ABERTURAS = [
    "No dia {data}, durante {periodo}, no(a) {local}, foi registrada ocorrência disciplinar envolvendo {alunos}, da turma {turma}.",
    "Aos {data}, no período {periodo}, nas dependências do(a) {local}, lavra-se o presente registro referente a {alunos}, estudante(s) da turma {turma}.",
    "Registra-se que, em {data}, durante {periodo}, no(a) {local}, houve ocorrência envolvendo {alunos}, da turma {turma}.",
]

FATOS = [
    "A ocorrência refere-se a {tipo}. Conforme relato apresentado, {relato}.",
    "O fato registrado foi classificado inicialmente como {tipo}, tendo sido informado que {relato}.",
    "Segundo os elementos relatados à coordenação, a situação envolveu {tipo}, nos seguintes termos: {relato}.",
]

ENQUADRAMENTOS = [
    "A conduta foi analisada à luz do Regimento Interno Escolar, especialmente o Art. {artigo}, inciso {inciso}, sendo classificada como {gravidade}, sujeita à sanção de {sancao}, nos termos do Art. 83.",
    "Considerando o Regimento Interno Escolar, o registro enquadra-se no Art. {artigo}, inciso {inciso}, com classificação disciplinar de {gravidade} e previsão de {sancao}.",
    "Para fins de acompanhamento, observa-se o disposto no Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, com indicação de {gravidade} e sanção disciplinar de {sancao}.",
]

ORIENTACOES = [
    "O(a) estudante foi orientado(a) quanto à necessidade de observar as normas de convivência escolar, mantendo conduta compatível com o ambiente educacional.",
    "Foi realizada orientação pedagógica ao(à) estudante, reforçando o respeito às normas regimentais, aos servidores e aos demais integrantes da comunidade escolar.",
    "A coordenação prestou orientação formal, destacando a importância da responsabilidade, do respeito e da preservação da rotina escolar.",
]

PROVIDENCIAS = [
    "Como providência adotada, registra-se: {providencias}.",
    "Diante do ocorrido, foram adotadas as seguintes providências: {providencias}.",
    "Para encaminhamento da situação, ficou registrado: {providencias}.",
]

FECHAMENTOS = [
    "Fica lavrada a presente ata para fins de registro, acompanhamento e demais providências cabíveis.",
    "Nada mais havendo a registrar neste ato, firma-se a presente ata para acompanhamento pela unidade escolar.",
    "O presente registro permanece arquivado para acompanhamento pedagógico e disciplinar, sem prejuízo de novas providências se necessárias.",
]

CONTEXTOS = [
    "O registro considera as informações prestadas no momento da ocorrência e poderá ser complementado caso surjam novos elementos.",
    "A situação foi registrada com base no relato apresentado à unidade escolar, preservando-se o caráter pedagógico do acompanhamento.",
    "A lavratura desta ata busca documentar o ocorrido de forma clara, permitindo acompanhamento pela equipe escolar.",
]

ENCAMINHAMENTOS_PEDAGOGICOS = [
    "Recomenda-se acompanhamento pela coordenação, com retomada das orientações em momento oportuno e registro de eventual evolução do caso.",
    "A equipe escolar deverá observar a resposta do(a) estudante às orientações realizadas, buscando prevenir novas ocorrências.",
    "A situação poderá ser retomada em atendimento individual ou reunião pedagógica, conforme avaliação da coordenação.",
]

CIENCIA = [
    "Os envolvidos foram cientificados de que o registro tem finalidade disciplinar e pedagógica.",
    "Foi esclarecido que a ata integra os registros escolares e servirá de referência para acompanhamento posterior.",
    "A unidade escolar reforçou que novas ocorrências poderão ensejar providências regimentais adicionais.",
]

MESES = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}

ESTILOS_VALIDOS = {"modelo_escola", "equilibrada", "objetiva", "detalhada", "pedagogica"}


def formatar_data(data_ocorrencia: date) -> str:
    return data_ocorrencia.strftime("%d/%m/%Y")


def formatar_data_extenso(data_ocorrencia: date) -> str:
    return f"{data_ocorrencia.day} de {MESES[data_ocorrencia.month]} de {data_ocorrencia.year}"


def normalizar_estilo(estilo: str | None) -> str:
    estilo = (estilo or "modelo_escola").strip().lower()
    return estilo if estilo in ESTILOS_VALIDOS else "modelo_escola"


def garantir_ponto(texto: str) -> str:
    texto = texto.strip()
    if not texto:
        return texto
    if texto.endswith((".", "!", "?")):
        return texto
    return f"{texto}."


def local_preposicionado(local: str) -> str:
    local = local.strip()
    primeiras = local.lower().split(maxsplit=1)[0] if local else ""
    if primeiras in {"em", "no", "na", "nos", "nas"}:
        return local
    return f"em {local}"


def texto_responsavel(convocado: bool, nome_responsavel: str | None) -> str:
    if convocado and nome_responsavel:
        return f"O(a) responsável {nome_responsavel} foi convocado(a) para ciência e acompanhamento da situação."
    if convocado:
        return "O(a) responsável foi convocado(a) para ciência e acompanhamento da situação."
    return "Não houve convocação de responsável neste registro, permanecendo a situação sob acompanhamento da coordenação."


def texto_reincidencia(reincidencia: bool) -> str:
    if reincidencia:
        return "Consta indicação de reincidência, devendo o caso receber atenção específica nos registros de acompanhamento escolar."
    return "Não foi indicada reincidência no momento da lavratura deste registro."


def montar_partes_equilibrada(rng: random.Random, contexto: dict, dados: dict, regra) -> list[str]:
    partes = [
        rng.choice(ABERTURAS).format(**contexto),
        rng.choice(FATOS).format(**contexto),
    ]

    if rng.choice([True, False]):
        partes.append(rng.choice(CONTEXTOS))

    partes.extend(
        [
            rng.choice(ENQUADRAMENTOS).format(**contexto),
            rng.choice(ORIENTACOES),
            regra.orientacao,
            rng.choice(PROVIDENCIAS).format(**contexto),
            texto_responsavel(dados["responsavel_convocado"], dados.get("nome_responsavel")),
            texto_reincidencia(dados["reincidencia"]),
        ]
    )
    return partes


def montar_partes_modelo_escola(rng: random.Random, contexto: dict, dados: dict, regra) -> list[str]:
    responsavel = dados.get("nome_responsavel")
    if dados["responsavel_convocado"] and responsavel:
        trecho_responsavel = (
            f"O(a) responsável legal, {responsavel}, deverá comparecer à escola para tomar ciência formal "
            "da ocorrência, acompanhar os encaminhamentos e reforçar, junto ao(à) estudante, as orientações "
            "necessárias quanto à conduta esperada no ambiente escolar."
        )
    elif dados["responsavel_convocado"]:
        trecho_responsavel = (
            "O(a) responsável legal deverá comparecer à escola para tomar ciência formal da ocorrência, "
            "acompanhar os encaminhamentos e reforçar as orientações necessárias quanto à conduta esperada "
            "no ambiente escolar."
        )
    else:
        trecho_responsavel = (
            "Neste momento, a situação permaneceu sob acompanhamento da equipe escolar, sem convocação "
            "imediata de responsável legal."
        )

    reincidencia = (
        "Foi ressaltado que a reincidência poderá acarretar novas medidas disciplinares previstas no "
        "regimento escolar, conforme avaliação da equipe gestora."
        if dados["reincidencia"]
        else "Foi ressaltado que atitudes dessa natureza poderão acarretar medidas disciplinares previstas no regimento escolar, especialmente em caso de reincidência."
    )

    texto = (
        "No dia {data_extenso}, durante {periodo}, {local}, foi registrada ocorrência envolvendo "
        "{alunos}, da turma {turma}, referente a {tipo}. Conforme informações "
        "registradas pela equipe escolar, {relato} A situação foi acompanhada pela equipe gestora, "
        "que realizou a averiguação dos fatos e orientou os envolvidos quanto à gravidade da conduta, "
        "considerando o descumprimento das normas de convivência e a necessidade de preservação de um "
        "ambiente seguro, saudável e adequado ao desenvolvimento dos estudantes. A equipe gestora esclareceu "
        "que a unidade escolar tem o dever de zelar pelo cumprimento do regimento interno e pela integridade "
        "física, emocional e disciplinar da comunidade escolar. Para fins de registro e acompanhamento, "
        "a conduta foi analisada à luz do Regimento Interno Escolar, especialmente o Art. {artigo}, inciso "
        "{inciso}, sendo classificada como {gravidade}, com previsão de {sancao}. {reincidencia} Diante dos fatos, registra-se "
        "como providência adotada: {providencias} Como orientação específica, registrou-se: {orientacao} "
        "{trecho_responsavel} Os envolvidos "
        "permaneceram cientes das orientações recebidas e foram advertidos quanto à "
        "necessidade de respeitar as normas da instituição, mantendo comportamento adequado e compatível com "
        "os princípios de convivência escolar. Ficou registrado em ata o ocorrido para acompanhamento e "
        "providências cabíveis por parte da escola."
    ).format(
        data_extenso=contexto["data_extenso"],
        periodo=contexto["periodo"],
        local=local_preposicionado(contexto["local"]),
        alunos=contexto["alunos"],
        turma=contexto["turma"],
        tipo=contexto["tipo"].lower(),
        relato=garantir_ponto(contexto["relato"]),
        artigo=contexto["artigo"],
        inciso=contexto["inciso"],
        gravidade=contexto["gravidade"],
        sancao=contexto["sancao"],
        reincidencia=reincidencia,
        providencias=garantir_ponto(contexto["providencias"]),
        orientacao=garantir_ponto(regra.orientacao),
        trecho_responsavel=trecho_responsavel,
    )

    return [texto]


def montar_partes_objetiva(rng: random.Random, contexto: dict, dados: dict, regra) -> list[str]:
    return [
        (
            "Aos {data}, durante {periodo}, no(a) {local}, registra-se ocorrência "
            "envolvendo {alunos}, da turma {turma}, classificada como {tipo}."
        ).format(**contexto),
        f"Relato dos fatos: {garantir_ponto(contexto['relato'])}",
        (
            "Enquadramento sugerido: Art. {artigo}, inciso {inciso}, "
            "{gravidade}, com previsão de {sancao}."
        ).format(**contexto),
        f"Providências: {garantir_ponto(contexto['providencias'])}",
        texto_responsavel(dados["responsavel_convocado"], dados.get("nome_responsavel")),
        texto_reincidencia(dados["reincidencia"]),
        rng.choice(FECHAMENTOS),
    ]


def montar_partes_detalhada(rng: random.Random, contexto: dict, dados: dict, regra) -> list[str]:
    return [
        rng.choice(ABERTURAS).format(**contexto),
        rng.choice(CONTEXTOS),
        (
            "Conforme relato apresentado à coordenação, a situação foi descrita da seguinte forma: "
            f"{garantir_ponto(contexto['relato'])}"
        ),
        (
            "A ocorrência foi registrada como {tipo}. Após análise inicial, observou-se o disposto "
            "no Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, com classificação de "
            "{gravidade} e sanção prevista de {sancao}."
        ).format(**contexto),
        f"Quanto aos encaminhamentos imediatos, registra-se que {garantir_ponto(contexto['providencias'])}",
        rng.choice(ORIENTACOES),
        regra.orientacao,
        rng.choice(CIENCIA),
        texto_responsavel(dados["responsavel_convocado"], dados.get("nome_responsavel")),
        texto_reincidencia(dados["reincidencia"]),
    ]


def montar_partes_pedagogica(rng: random.Random, contexto: dict, dados: dict, regra) -> list[str]:
    return [
        rng.choice(ABERTURAS).format(**contexto),
        (
            "A situação envolveu {tipo}. O relato encaminhado à unidade escolar informa que "
            f"{garantir_ponto(contexto['relato'])}"
        ).format(**contexto),
        rng.choice(ORIENTACOES),
        regra.orientacao,
        rng.choice(ENCAMINHAMENTOS_PEDAGOGICOS),
        rng.choice(ENQUADRAMENTOS).format(**contexto),
        rng.choice(PROVIDENCIAS).format(**contexto),
        texto_responsavel(dados["responsavel_convocado"], dados.get("nome_responsavel")),
        texto_reincidencia(dados["reincidencia"]),
    ]


def gerar_ata(dados: dict, regra, seed: int | None = None) -> str:
    rng = random.Random(seed)
    estilo = normalizar_estilo(dados.get("estilo_redacao"))
    contexto = {
        "data": formatar_data(dados["data_ocorrencia"]),
        "data_extenso": formatar_data_extenso(dados["data_ocorrencia"]),
        "periodo": dados["periodo"],
        "local": dados["local"],
        "alunos": dados["alunos"],
        "turma": dados["turma"],
        "tipo": dados["tipo_ocorrencia"],
        "relato": dados["relato_simples"].strip(),
        "providencias": dados["providencias"].strip(),
        "artigo": regra.artigo,
        "inciso": regra.inciso,
        "gravidade": regra.gravidade.lower(),
        "sancao": regra.sancao.lower(),
    }

    montadores = {
        "modelo_escola": montar_partes_modelo_escola,
        "equilibrada": montar_partes_equilibrada,
        "objetiva": montar_partes_objetiva,
        "detalhada": montar_partes_detalhada,
        "pedagogica": montar_partes_pedagogica,
    }
    partes = montadores[estilo](rng, contexto, dados, regra)

    observacoes = dados.get("observacoes_adicionais")
    if observacoes:
        partes.append(f"Observações adicionais: {observacoes.strip()}.")

    if estilo not in {"modelo_escola", "objetiva"}:
        partes.append(rng.choice(FECHAMENTOS))
    return "\n\n".join(partes)
