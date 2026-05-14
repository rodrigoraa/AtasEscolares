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

ABERTURAS_MODELO_ESCOLA = [
    "No dia {data_extenso}, durante {periodo}, {local}, foi registrada ocorrência envolvendo {alunos}, da turma {turma}, referente a {tipo}.",
    "Segundo relato da equipe escolar, no dia {data_extenso}, durante {periodo}, {local}, houve ocorrência envolvendo {alunos}, da turma {turma}, relacionada a {tipo}.",
    "Foi constatado pela equipe gestora que, em {data_extenso}, durante {periodo}, {local}, ocorreu situação disciplinar envolvendo {alunos}, da turma {turma}, referente a {tipo}.",
    "Durante acompanhamento realizado pela coordenação em {data_extenso}, no período {periodo}, {local}, registrou-se ocorrência envolvendo {alunos}, da turma {turma}, relacionada a {tipo}.",
    "Em verificação realizada pela gestão escolar no dia {data_extenso}, durante {periodo}, {local}, foi identificado registro disciplinar envolvendo {alunos}, da turma {turma}, relacionado a {tipo}.",
    "Após comunicação à coordenação, registrou-se que, em {data_extenso}, durante {periodo}, {local}, houve situação envolvendo {alunos}, da turma {turma}, referente a {tipo}.",
    "Conforme registro interno da unidade escolar, em {data_extenso}, no período {periodo}, {local}, ocorreu fato disciplinar envolvendo {alunos}, da turma {turma}, relacionado a {tipo}.",
    "No acompanhamento da rotina escolar em {data_extenso}, durante {periodo}, {local}, foi relatada ocorrência envolvendo {alunos}, da turma {turma}, quanto a {tipo}.",
    "Aos {data_extenso}, no período {periodo}, {local}, a {ator} registrou situação disciplinar envolvendo {alunos}, da turma {turma}, referente a {tipo}.",
    "Em atendimento realizado no âmbito escolar, referente ao dia {data_extenso}, durante {periodo}, {local}, foi formalizado registro envolvendo {alunos}, da turma {turma}, por situação relacionada a {tipo}.",
]

RELATOS_MODELO_ESCOLA = [
    "Conforme informações registradas pela equipe escolar, {relato}",
    "De acordo com o relato encaminhado à coordenação, {relato}",
    "A situação foi descrita à equipe gestora nos seguintes termos: {relato}",
    "No registro dos fatos, consta que {relato}",
    "Segundo relato encaminhado à coordenação, {relato}",
    "Durante a apuração inicial, foi informado que {relato}",
    "Em registro apresentado à {ator}, consta que {relato}",
    "A partir das informações colhidas pela unidade escolar, registrou-se que {relato}",
    "Conforme comunicação feita à equipe pedagógica, {relato}",
    "Na descrição do ocorrido, foi apontado que {relato}",
]

INTERVENCOES_MODELO_ESCOLA = [
    "A situação foi acompanhada pela equipe gestora, que realizou a averiguação dos fatos e orientou os envolvidos quanto à gravidade da conduta.",
    "Em orientação posterior ao ocorrido, a coordenação reforçou aos envolvidos a necessidade de observância das normas de convivência escolar.",
    "A equipe escolar interveio de forma imediata, promovendo orientação formal e registrando a necessidade de conduta compatível com o ambiente educacional.",
    "Após a ciência do ocorrido, a coordenação procedeu aos encaminhamentos necessários e orientou os envolvidos quanto às consequências regimentais da conduta.",
    "Após intervenção da equipe pedagógica, foram prestadas orientações sobre a conduta esperada no ambiente escolar.",
    "A gestão escolar realizou os encaminhamentos iniciais e reforçou a necessidade de respeito às normas internas.",
    "A coordenação acompanhou a situação e orientou os envolvidos quanto aos impactos da conduta na rotina escolar.",
    "Durante a verificação dos fatos, a {ator} registrou a ocorrência e adotou as medidas de orientação cabíveis.",
    "A equipe gestora dialogou com os envolvidos e esclareceu os deveres previstos para a convivência escolar.",
]

DEVER_ESCOLA_MODELO = [
    "A unidade escolar ressaltou seu dever de zelar por um ambiente seguro, saudável e adequado ao desenvolvimento dos estudantes.",
    "Foi reforçado que o cumprimento das normas internas contribui para a preservação da integridade física, emocional e disciplinar da comunidade escolar.",
    "A equipe gestora destacou a importância da responsabilidade individual e coletiva para a manutenção da rotina escolar.",
]

ENQUADRAMENTOS_MODELO_ESCOLA = [
    "Para fins de registro e acompanhamento, a conduta foi analisada à luz do Regimento Interno Escolar, especialmente o Art. {artigo}, inciso {inciso}, sendo classificada como {gravidade}, com previsão de {sancao}.",
    "Considerando o Regimento Interno Escolar, observou-se o enquadramento no Art. {artigo}, inciso {inciso}, com classificação de {gravidade} e previsão de {sancao}.",
    "O registro foi relacionado ao disposto no Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, com indicação de {gravidade} e sanção prevista de {sancao}.",
    "No que se refere ao enquadramento disciplinar, aplica-se o disposto no Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, caracterizando {gravidade} e indicando {sancao}.",
    "A situação foi vinculada ao Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, com natureza de {gravidade} e encaminhamento disciplinar correspondente a {sancao}.",
    "Nos termos do Regimento Interno Escolar, o fato guarda relação com o Art. {artigo}, inciso {inciso}, sendo tratado como {gravidade}, com previsão de {sancao}.",
    "Para a adequada formalização do registro, considerou-se o Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, classificando-se a ocorrência como {gravidade} e prevendo-se {sancao}.",
]

PROVIDENCIAS_MODELO_ESCOLA = [
    "Diante dos fatos, registra-se como providência adotada: {providencias}",
    "Como encaminhamento imediato, ficou registrado que {providencias}",
    "Para acompanhamento da situação, a providência tomada foi a seguinte: {providencias}",
    "Quanto às medidas adotadas pela escola, registra-se que {providencias}",
]

ORIENTACOES_MODELO_ESCOLA = [
    "Como orientação específica, registrou-se: {orientacao}",
    "Na ocasião, reforçou-se a seguinte orientação: {orientacao}",
    "A orientação pedagógica aplicada ao caso foi: {orientacao}",
]

CIENCIA_MODELO_ESCOLA = [
    "Os envolvidos permaneceram cientes das orientações recebidas e foram advertidos quanto à necessidade de respeitar as normas da instituição.",
    "Foi dada ciência aos envolvidos sobre a importância de manter comportamento adequado e compatível com os princípios de convivência escolar.",
    "A coordenação reforçou aos envolvidos que novas ocorrências poderão ensejar providências regimentais adicionais.",
    "Os estudantes foram orientados a observar as normas escolares e a manter postura compatível com o ambiente educacional.",
    "A {ator} registrou a ciência dos envolvidos quanto às orientações prestadas e aos possíveis desdobramentos regimentais.",
    "Foi reforçada a necessidade de responsabilidade individual, respeito às regras internas e colaboração com a rotina escolar.",
]

FECHAMENTOS_MODELO_ESCOLA = [
    "Ficou registrado em ata o ocorrido para acompanhamento e providências cabíveis por parte da escola.",
    "Lavra-se o presente registro para fins de acompanhamento pedagógico e disciplinar pela unidade escolar.",
    "O presente registro fica arquivado para acompanhamento da equipe escolar e adoção de novas providências, se necessárias.",
    "Nada mais havendo a registrar neste ato, firma-se a presente ata para os devidos fins escolares.",
    "Registra-se a presente ocorrência para acompanhamento da coordenação e consulta nos registros escolares, quando necessário.",
    "A presente ata é lavrada para documentar o ocorrido e subsidiar os encaminhamentos pedagógicos e disciplinares cabíveis.",
    "O registro permanece à disposição da equipe gestora para acompanhamento e eventual adoção de novas medidas.",
    "Assim, formaliza-se o presente registro para ciência, arquivo e acompanhamento pela unidade escolar.",
]

REINCIDENCIAS_MODELO_ESCOLA = [
    "Foi ressaltado que novas ocorrências poderão motivar medidas disciplinares adicionais previstas no regimento escolar.",
    "A {ator} informou que eventual repetição da conduta poderá resultar em novos encaminhamentos regimentais.",
    "Registrou-se que a continuidade de atitudes semelhantes poderá ensejar providências disciplinares complementares.",
    "Foi esclarecido que a reincidência será considerada em futuros acompanhamentos pedagógicos e disciplinares.",
]

REINCIDENCIAS_CONFIRMADAS_MODELO_ESCOLA = [
    "Considerando a indicação de reincidência, o caso deverá receber acompanhamento específico pela equipe escolar.",
    "Por haver registro de reincidência, a situação será acompanhada com atenção pela coordenação.",
    "A reincidência informada foi registrada para subsidiar eventuais encaminhamentos pedagógicos e disciplinares.",
]

ATORES_INSTITUCIONAIS = [
    "coordenação",
    "equipe gestora",
    "equipe escolar",
    "gestão escolar",
    "equipe pedagógica",
]

ABERTURAS_NARRATIVAS = [
    "No dia {data_extenso}, {periodo}, {local}, foi registrada ocorrência disciplinar envolvendo {alunos}, da turma {turma}, referente a {tipo}.",
    "Aos {data_extenso}, {periodo}, {local}, lavra-se o presente registro referente a {alunos}, da turma {turma}, em razão de ocorrência relacionada a {tipo}.",
    "Em {data_extenso}, {periodo}, {local}, a {ator} registrou ocorrência disciplinar envolvendo {alunos}, estudante(s) da turma {turma}, referente a {tipo}.",
    "No dia {data_extenso}, {periodo}, {local}, foi formalizado registro envolvendo {alunos}, da turma {turma}, em situação classificada como {tipo}.",
    "Conforme registro interno da unidade escolar, em {data_extenso}, {periodo}, {local}, houve ocorrência envolvendo {alunos}, da turma {turma}, relacionada a {tipo}.",
]

RELATOS_NARRATIVOS = [
    "Segundo relato encaminhado à coordenação, {relato}",
    "Conforme informações registradas pela equipe escolar, {relato}",
    "De acordo com o registro dos fatos, {relato}",
    "Na descrição apresentada à {ator}, consta que {relato}",
    "A partir das informações colhidas pela unidade escolar, registrou-se que {relato}",
]

AVERIGUACOES_NARRATIVAS = [
    "Após tomar ciência da situação, a {ator} realizou a averiguação inicial, abordou os envolvidos e buscou esclarecer as circunstâncias do ocorrido.",
    "A {ator}, ao verificar o fato, procedeu à abordagem dos envolvidos e registrou as informações necessárias para o acompanhamento escolar.",
    "Diante do registro, a {ator} realizou intervenção junto aos envolvidos, com o objetivo de apurar a situação e orientar quanto aos encaminhamentos cabíveis.",
    "Em seguida, a {ator} acompanhou a situação, realizou a verificação dos fatos e adotou os encaminhamentos iniciais pertinentes.",
]

ORIENTACOES_NARRATIVAS = [
    "Na ocasião, os envolvidos foram orientados quanto à gravidade da conduta, à necessidade de observância das normas de convivência e à preservação de um ambiente escolar seguro e adequado ao desenvolvimento dos estudantes.",
    "A {ator} orientou os envolvidos sobre a seriedade do ocorrido, destacando os cuidados com a saúde, a segurança no ambiente escolar e o respeito às regras de convivência da unidade.",
    "Foi realizada orientação pedagógica aos envolvidos, ressaltando que a conduta registrada compromete a organização da rotina escolar e exige responsabilidade no cumprimento das normas internas.",
    "Em orientação posterior ao ocorrido, a {ator} destacou a importância da convivência respeitosa, da preservação da saúde e do cumprimento das normas escolares.",
]

REGIMENTOS_NARRATIVOS = [
    "Para fins de registro e acompanhamento, a conduta foi analisada à luz do Regimento Interno Escolar, especialmente o Art. {artigo}, inciso {inciso}, sendo classificada como {gravidade}, com previsão de {sancao}.",
    "Nos termos do Regimento Interno Escolar, o fato guarda relação com o Art. {artigo}, inciso {inciso}, sendo classificado como {gravidade}, com sanção prevista de {sancao}.",
    "Considerando o Regimento Interno Escolar, observou-se o enquadramento no Art. {artigo}, inciso {inciso}, caracterizando {gravidade} e indicando como medida disciplinar prevista a {sancao}.",
    "O registro foi relacionado ao disposto no Art. {artigo}, inciso {inciso}, do Regimento Interno Escolar, com classificação de {gravidade} e previsão de {sancao}.",
]

PROVIDENCIAS_NARRATIVAS = [
    "Como providência adotada pela unidade escolar, registra-se que {providencias}",
    "Quanto às medidas tomadas, ficou registrado que {providencias}",
    "Para encaminhamento da situação, a providência registrada foi: {providencias}",
    "No acompanhamento do caso, a medida adotada pela escola foi a seguinte: {providencias}",
]

RESPONSAVEIS_NARRATIVOS = [
    "{responsavel} para tomar ciência formal da ocorrência, acompanhar os encaminhamentos e reforçar, junto ao(à) estudante, as orientações necessárias quanto à conduta esperada no ambiente escolar.",
    "{responsavel} a fim de tomar ciência do registro, participar dos encaminhamentos realizados pela escola e colaborar no acompanhamento da conduta do(a) estudante.",
    "{responsavel} para ciência da situação registrada, diálogo com a {ator} e acompanhamento das providências pedagógicas e disciplinares cabíveis.",
]

ENCERRAMENTOS_NARRATIVOS = [
    "Os envolvidos permaneceram cientes das orientações recebidas, ficando a presente ata lavrada para registro, acompanhamento e providências cabíveis por parte da unidade escolar.",
    "Nada mais havendo a registrar neste ato, firma-se a presente ata para ciência, arquivo e acompanhamento pela equipe escolar.",
    "O presente registro fica arquivado na unidade escolar para acompanhamento pedagógico e disciplinar, sem prejuízo de novas providências, se necessárias.",
    "Lavra-se a presente ata para documentar o ocorrido e subsidiar os encaminhamentos escolares pertinentes.",
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
    texto = limpar_campo(texto)
    if not texto:
        return texto
    if texto.endswith((".", "!", "?")):
        return texto
    return f"{texto}."


def limpar_campo(valor, padrao: str = "") -> str:
    if valor is None:
        return padrao
    texto = str(valor).strip()
    if texto.lower() in {"none", "null", "undefined", "nan"}:
        return padrao
    texto = " ".join(texto.split())
    return texto or padrao


def limpar_contexto(contexto: dict) -> dict:
    return {
        chave: limpar_campo(valor)
        for chave, valor in contexto.items()
    }


def limpar_frase(texto: str) -> str:
    texto = limpar_campo(texto)
    texto = texto.replace(" ,", ",").replace(" .", ".")
    texto = texto.replace("..", ".")
    texto = texto.replace(" ,", ",")
    return garantir_ponto(texto)


def local_preposicionado(local: str) -> str:
    local = limpar_campo(local, "na unidade escolar")
    primeiras = local.lower().split(maxsplit=1)[0] if local else ""
    if primeiras in {"em", "no", "na", "nos", "nas"}:
        return local
    return f"em {local}"


def periodo_narrativo(periodo: str) -> str:
    periodo = limpar_campo(periodo, "período não informado")
    if periodo.lower() in {"matutino", "vespertino", "noturno", "integral"}:
        return f"no período {periodo}"
    return f"durante {periodo}"


def texto_responsavel(convocado: bool, nome_responsavel: str | None) -> str:
    nome_responsavel = limpar_campo(nome_responsavel)
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


def montar_partes_modelo_escola(
    rng: random.Random,
    contexto: dict,
    dados: dict,
    regra,
    contextos_banco: list[str] | None = None,
) -> list[str]:
    contexto = limpar_contexto(contexto)
    ator = rng.choice(ATORES_INSTITUCIONAIS)
    contexto_modelo = {
        **contexto,
        "local": local_preposicionado(contexto["local"]),
        "periodo": periodo_narrativo(contexto["periodo"]),
        "tipo": contexto["tipo"].lower(),
        "ator": ator,
    }
    contexto_relato = {
        **contexto_modelo,
        "relato": garantir_ponto(contexto["relato"]),
    }

    responsavel = limpar_campo(dados.get("nome_responsavel"))
    if responsavel:
        chamada_responsavel = f"O(a) responsável legal, {responsavel}, deverá comparecer à escola"
    else:
        chamada_responsavel = "O(a) responsável legal deverá comparecer à escola"

    abertura = rng.choice(ABERTURAS_NARRATIVAS).format(**contexto_modelo)
    relato = rng.choice(RELATOS_NARRATIVOS).format(**contexto_relato)
    averiguacao = rng.choice(AVERIGUACOES_NARRATIVAS).format(ator=ator)

    textos_contexto = " ".join(
        limpar_frase(texto)
        for texto in (contextos_banco or [])
        if limpar_campo(texto)
    )
    orientacao = rng.choice(ORIENTACOES_NARRATIVAS).format(ator=ator)
    if textos_contexto:
        orientacao = f"{orientacao} {textos_contexto}"

    regimento = rng.choice(REGIMENTOS_NARRATIVOS).format(**contexto)
    providencia = rng.choice(PROVIDENCIAS_NARRATIVAS).format(
        providencias=limpar_frase(contexto["providencias"])
    )
    responsavel_texto = rng.choice(RESPONSAVEIS_NARRATIVOS).format(
        responsavel=chamada_responsavel,
        ator=ator,
    )
    encerramento = rng.choice(ENCERRAMENTOS_NARRATIVOS)

    return [
        limpar_frase(abertura),
        limpar_frase(relato),
        limpar_frase(averiguacao),
        limpar_frase(orientacao),
        limpar_frase(regimento),
        limpar_frase(providencia),
        limpar_frase(responsavel_texto),
        limpar_frase(encerramento),
    ]


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


def gerar_ata(
    dados: dict,
    regra,
    seed: int | None = None,
    contextos: list[str] | None = None,
) -> str:
    rng = random.Random(seed)
    estilo = normalizar_estilo(dados.get("estilo_redacao"))
    contexto = {
        "data": formatar_data(dados["data_ocorrencia"]),
        "data_extenso": formatar_data_extenso(dados["data_ocorrencia"]),
        "periodo": limpar_campo(dados.get("periodo"), "período não informado"),
        "local": limpar_campo(dados.get("local"), "unidade escolar"),
        "alunos": limpar_campo(dados.get("alunos"), "estudante(s) envolvido(s)"),
        "turma": limpar_campo(dados.get("turma"), "turma não informada"),
        "tipo": limpar_campo(dados.get("tipo_ocorrencia"), "ocorrência disciplinar"),
        "relato": limpar_campo(dados.get("relato_simples"), "os fatos foram registrados pela equipe escolar"),
        "providencias": limpar_campo(dados.get("providencias"), "foram adotadas as providências cabíveis pela unidade escolar"),
        "artigo": limpar_campo(regra.artigo),
        "inciso": limpar_campo(regra.inciso),
        "gravidade": limpar_campo(regra.gravidade).lower(),
        "sancao": limpar_campo(regra.sancao).lower(),
    }

    montadores = {
        "modelo_escola": montar_partes_modelo_escola,
        "equilibrada": montar_partes_equilibrada,
        "objetiva": montar_partes_objetiva,
        "detalhada": montar_partes_detalhada,
        "pedagogica": montar_partes_pedagogica,
    }
    if estilo == "modelo_escola":
        partes = montar_partes_modelo_escola(rng, contexto, dados, regra, contextos)
    else:
        partes = montadores[estilo](rng, contexto, dados, regra)

    observacoes = limpar_campo(dados.get("observacoes_adicionais"))
    if observacoes:
        partes.append(f"Observações adicionais: {garantir_ponto(observacoes)}")

    if estilo not in {"modelo_escola", "objetiva"}:
        partes.append(rng.choice(FECHAMENTOS))
    return "\n\n".join(partes)
