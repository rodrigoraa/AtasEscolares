from fastapi import Depends, HTTPException, Request, status
import bcrypt
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def criar_admin_padrao(db: Session) -> None:
    existe = db.query(Usuario).filter(Usuario.usuario == "admin").first()
    if existe:
        return

    db.add(
        Usuario(
            nome="Administrador",
            usuario="admin",
            senha_hash=hash_password("admin123"),
        )
    )
    db.commit()


def autenticar_usuario(db: Session, usuario: str, senha: str) -> Usuario | None:
    user = db.query(Usuario).filter(Usuario.usuario == usuario).first()
    if not user or not verify_password(senha, user.senha_hash):
        return None
    return user


def usuario_logado(request: Request, db: Session = Depends(get_db)) -> Usuario:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )

    user = db.get(Usuario, user_id)
    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )
    return user
