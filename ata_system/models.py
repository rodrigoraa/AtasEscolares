from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text

from database import Base


class Ata(Base):
    __tablename__ = "atas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(30), nullable=False)
    ano = Column(Integer, nullable=False)
    data_ocorrencia = Column(Date, nullable=False)
    periodo = Column(String(100), nullable=False)
    local = Column(String(150), nullable=False)
    alunos = Column(Text, nullable=False)
    turma = Column(String(80), nullable=False)
    tipo_ocorrencia = Column(String(180), nullable=False)
    relato_simples = Column(Text, nullable=False)
    providencias = Column(Text, nullable=False)
    responsavel_convocado = Column(Boolean, default=False)
    nome_responsavel = Column(String(180), nullable=True)
    reincidencia = Column(Boolean, default=False)
    artigo = Column(String(20), nullable=False)
    inciso = Column(String(20), nullable=False)
    gravidade = Column(String(80), nullable=False)
    sancao = Column(String(180), nullable=False)
    texto_gerado = Column(Text, nullable=False)
    assinaturas = Column(Text, nullable=False, default="")
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    usuario = Column(String(80), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
