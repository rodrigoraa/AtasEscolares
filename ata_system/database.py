from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'atas.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Importa os models para registrar as tabelas no Base.metadata.
    from models import Ata, ContextoAta, Usuario  # noqa: F401

    Base.metadata.create_all(bind=engine)
    migrar_colunas()


def migrar_colunas():
    inspector = inspect(engine)
    if "atas" not in inspector.get_table_names():
        return

    colunas = {coluna["name"] for coluna in inspector.get_columns("atas")}
    with engine.begin() as conn:
        if "assinaturas" not in colunas:
            conn.execute(text("ALTER TABLE atas ADD COLUMN assinaturas TEXT NOT NULL DEFAULT ''"))
