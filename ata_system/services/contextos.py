import re

from sqlalchemy.orm import Session

from models import ContextoAta


CONTEXTOS_INICIAIS = [
    {
        "titulo": "Uso de dispositivo eletrônico para fumar",
        "tipo_ocorrencia": "Fumo ou cigarro eletrônico",
        "gravidade": "Falta moderada",
        "palavras_chave": "cigarro eletrônico vape fumar dispositivo saúde sala colegas",
        "texto": (
            "A unidade escolar reforçou que o porte ou uso de dispositivos eletrônicos para fumar "
            "não é permitido no ambiente escolar, por representar risco à saúde e contrariar as normas "
            "de convivência e segurança da comunidade escolar."
        ),
    },
    {
        "titulo": "Preservação do patrimônio escolar",
        "tipo_ocorrencia": "Dano ao patrimônio",
        "gravidade": "Falta grave",
        "palavras_chave": "patrimônio dano quebra parede carteira porta reparação",
        "texto": (
            "Foi destacada a necessidade de preservação do patrimônio público escolar, bem como a "
            "responsabilidade dos estudantes quanto ao uso adequado dos espaços, materiais e equipamentos "
            "disponibilizados pela unidade."
        ),
    },
    {
        "titulo": "Convivência e respeito",
        "tipo_ocorrencia": None,
        "gravidade": "Falta grave",
        "palavras_chave": "ofensa agressão desacato respeito convivência servidor colega",
        "texto": (
            "A equipe escolar reforçou que a convivência no ambiente educacional deve ser pautada pelo "
            "respeito mútuo, diálogo e preservação da integridade física e emocional de todos os integrantes "
            "da comunidade escolar."
        ),
    },
    {
        "titulo": "Uso pedagógico de celular",
        "tipo_ocorrencia": "Uso de celular em sala",
        "gravidade": "Falta leve",
        "palavras_chave": "celular aparelho telefone sala aula autorização professor",
        "texto": (
            "Foi esclarecido que aparelhos celulares e similares somente devem ser utilizados quando houver "
            "autorização expressa para finalidade pedagógica, preservando-se a atenção, a organização da aula "
            "e o direito de aprendizagem dos estudantes."
        ),
    },
]


def normalizar(texto: str | None) -> set[str]:
    if not texto:
        return set()
    return {
        termo
        for termo in re.findall(r"[a-zA-ZÀ-ÿ0-9ºª]+", texto.lower())
        if len(termo) > 2
    }


def criar_contextos_iniciais(db: Session) -> None:
    if db.query(ContextoAta).first():
        return

    for contexto in CONTEXTOS_INICIAIS:
        db.add(ContextoAta(**contexto))
    db.commit()


def pontuar_contexto(contexto: ContextoAta, dados: dict, regra) -> int:
    pontos = 0
    if contexto.tipo_ocorrencia:
        if contexto.tipo_ocorrencia != dados["tipo_ocorrencia"]:
            return -1
        pontos += 8
    if contexto.gravidade and contexto.gravidade == regra.gravidade:
        pontos += 4

    texto_ocorrencia = " ".join(
        [
            dados.get("tipo_ocorrencia", ""),
            dados.get("relato_simples", ""),
            dados.get("providencias", ""),
            dados.get("observacoes_adicionais", "") or "",
        ]
    )
    termos_ocorrencia = normalizar(texto_ocorrencia)
    termos_contexto = normalizar(contexto.palavras_chave)
    pontos += min(len(termos_ocorrencia & termos_contexto), 6)
    return pontos


def selecionar_contextos(db: Session, dados: dict, regra, limite: int = 2) -> list[str]:
    candidatos = db.query(ContextoAta).filter(ContextoAta.ativo.is_(True)).all()
    pontuados = [
        (pontuar_contexto(contexto, dados, regra), contexto)
        for contexto in candidatos
    ]
    selecionados = [
        contexto.texto.strip()
        for pontos, contexto in sorted(pontuados, key=lambda item: item[0], reverse=True)
        if pontos > 0 and contexto.texto.strip()
    ]
    return selecionados[:limite]
