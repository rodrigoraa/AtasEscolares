from datetime import date
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from auth import autenticar_usuario, criar_admin_padrao, usuario_logado
from database import get_db, init_db
from models import Ata, Usuario
from services.assinaturas import (
    ASSINATURAS_PADRAO,
    desserializar_assinaturas,
    serializar_assinaturas,
)
from services.exportador_docx import exportar_ata_docx, exportar_ata_pdf
from services.gerador_ata import gerar_ata
from services.gerador_ia import GeracaoIAIndisponivel, gerar_ata_com_ia
from services.regras import sugerir_regra, tipos_ocorrencia


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="Sistema de Atas Disciplinares")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "troque-esta-chave-em-producao"),
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
AUTO_NUMERO_ATA = "__auto__"


@app.on_event("startup")
def startup() -> None:
    init_db()
    db = next(get_db())
    try:
        criar_admin_padrao(db)
    finally:
        db.close()


def form_bool(valor: str | None) -> bool:
    return valor == "sim"


def proximo_numero_ata(db: Session, ano: int) -> str:
    numeros = []
    atas_do_ano = db.query(Ata).filter(Ata.ano == ano).all()
    for ata in atas_do_ano:
        try:
            numeros.append(int(str(ata.numero).strip()))
        except ValueError:
            continue
    return str((max(numeros) if numeros else 0) + 1)


def dados_ata_form(
    numero: str,
    ano: int,
    data_ocorrencia: date,
    periodo: str,
    local: str,
    alunos: str,
    turma: str,
    tipo_ocorrencia: str,
    estilo_redacao: str,
    usar_ia: str | None,
    relato_simples: str,
    providencias: str,
    responsavel_convocado: str,
    nome_responsavel: str | None,
    reincidencia: str,
    observacoes_adicionais: str | None,
) -> dict:
    return {
        "numero": numero.strip(),
        "ano": ano,
        "data_ocorrencia": data_ocorrencia,
        "periodo": periodo.strip(),
        "local": local.strip(),
        "alunos": alunos.strip(),
        "turma": turma.strip(),
        "tipo_ocorrencia": tipo_ocorrencia.strip(),
        "estilo_redacao": estilo_redacao.strip() or "modelo_escola",
        "usar_ia": form_bool(usar_ia),
        "relato_simples": relato_simples.strip(),
        "providencias": providencias.strip(),
        "responsavel_convocado": form_bool(responsavel_convocado),
        "nome_responsavel": (nome_responsavel or "").strip() or None,
        "reincidencia": form_bool(reincidencia),
        "observacoes_adicionais": (observacoes_adicionais or "").strip(),
    }


@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "erro": None})


@app.post("/login")
def login(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    user = autenticar_usuario(db, usuario, senha)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Usuário ou senha inválidos."},
            status_code=401,
        )
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


@app.get("/")
def index(
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    atas = db.query(Ata).order_by(Ata.criado_em.desc()).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "atas": atas, "user": user}
    )


@app.get("/atas/nova")
def nova_ata_form(
    request: Request,
    user: Usuario = Depends(usuario_logado),
):
    return templates.TemplateResponse(
        "nova_ata.html",
        {
            "request": request,
            "tipos": tipos_ocorrencia(),
            "ano_atual": date.today().year,
            "assinaturas_padrao": ASSINATURAS_PADRAO,
            "user": user,
        },
    )


@app.post("/atas/gerar")
def gerar_previa_ata(
    request: Request,
    numero: str = Form(AUTO_NUMERO_ATA),
    ano: int = Form(...),
    data_ocorrencia: date = Form(...),
    periodo: str = Form(...),
    local: str = Form(...),
    alunos: str = Form(...),
    turma: str = Form(...),
    tipo_ocorrencia: str = Form(...),
    estilo_redacao: str = Form("modelo_escola"),
    usar_ia: str | None = Form(None),
    relato_simples: str = Form(...),
    providencias: str = Form(...),
    responsavel_convocado: str = Form("nao"),
    nome_responsavel: str | None = Form(None),
    reincidencia: str = Form("nao"),
    observacoes_adicionais: str | None = Form(None),
    assinaturas: list[str] | None = Form(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    numero = numero.strip() or AUTO_NUMERO_ATA
    dados = dados_ata_form(
        numero,
        ano,
        data_ocorrencia,
        periodo,
        local,
        alunos,
        turma,
        tipo_ocorrencia,
        estilo_redacao,
        usar_ia,
        relato_simples,
        providencias,
        responsavel_convocado,
        nome_responsavel,
        reincidencia,
        observacoes_adicionais,
    )
    regra = sugerir_regra(dados["tipo_ocorrencia"], dados["reincidencia"])
    aviso_geracao = None
    if dados["usar_ia"]:
        try:
            texto = gerar_ata_com_ia(dados, regra)
        except GeracaoIAIndisponivel as exc:
            texto = gerar_ata(dados, regra)
            aviso_geracao = f"Não foi possível usar IA: {exc} Foi gerada uma versão local."
    else:
        texto = gerar_ata(dados, regra)

    return templates.TemplateResponse(
        "editar_ata.html",
        {
            "request": request,
            "dados": dados,
            "regra": regra,
            "texto": texto,
            "aviso_geracao": aviso_geracao,
            "assinaturas_padrao": ASSINATURAS_PADRAO,
            "assinaturas_selecionadas": desserializar_assinaturas(serializar_assinaturas(assinaturas)),
            "user": user,
        },
    )


@app.post("/atas/salvar")
def salvar_ata(
    numero: str = Form(AUTO_NUMERO_ATA),
    ano: int = Form(...),
    data_ocorrencia: date = Form(...),
    periodo: str = Form(...),
    local: str = Form(...),
    alunos: str = Form(...),
    turma: str = Form(...),
    tipo_ocorrencia: str = Form(...),
    relato_simples: str = Form(...),
    providencias: str = Form(...),
    responsavel_convocado: str = Form("nao"),
    nome_responsavel: str | None = Form(None),
    reincidencia: str = Form("nao"),
    artigo: str = Form(...),
    inciso: str = Form(...),
    gravidade: str = Form(...),
    sancao: str = Form(...),
    texto_gerado: str = Form(...),
    assinaturas: list[str] | None = Form(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    numero = numero.strip()
    if not numero or numero == AUTO_NUMERO_ATA:
        numero = proximo_numero_ata(db, ano)

    ata = Ata(
        numero=numero,
        ano=ano,
        data_ocorrencia=data_ocorrencia,
        periodo=periodo,
        local=local,
        alunos=alunos,
        turma=turma,
        tipo_ocorrencia=tipo_ocorrencia,
        relato_simples=relato_simples,
        providencias=providencias,
        responsavel_convocado=form_bool(responsavel_convocado),
        nome_responsavel=nome_responsavel or None,
        reincidencia=form_bool(reincidencia),
        artigo=artigo,
        inciso=inciso,
        gravidade=gravidade,
        sancao=sancao,
        texto_gerado=texto_gerado.strip(),
        assinaturas=serializar_assinaturas(assinaturas),
    )
    db.add(ata)
    db.commit()
    db.refresh(ata)
    return RedirectResponse(f"/atas/{ata.id}", status_code=303)


@app.get("/atas/{ata_id}")
def visualizar_ata(
    request: Request,
    ata_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    ata = db.get(Ata, ata_id)
    if not ata:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return templates.TemplateResponse(
        "visualizar_ata.html",
        {
            "request": request,
            "ata": ata,
            "assinaturas": desserializar_assinaturas(ata.assinaturas),
            "user": user,
        },
    )


@app.get("/atas/{ata_id}/docx")
def baixar_docx(
    ata_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    ata = db.get(Ata, ata_id)
    if not ata:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    caminho = exportar_ata_docx(ata)
    return FileResponse(
        caminho,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=caminho.name,
    )


@app.get("/atas/{ata_id}/pdf")
def baixar_pdf(
    ata_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(usuario_logado),
):
    ata = db.get(Ata, ata_id)
    if not ata:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    caminho = exportar_ata_pdf(ata)
    return FileResponse(
        caminho,
        media_type="application/pdf",
        filename=caminho.name,
    )
