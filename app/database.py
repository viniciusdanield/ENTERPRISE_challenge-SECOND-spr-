from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

DATABASE_URL = "sqlite:///./chargeops.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def agora() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=agora)

    sessoes: Mapped[list["Sessao"]] = relationship(back_populates="usuario")


class Sessao(Base):
    __tablename__ = "sessoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    inicio: Mapped[datetime] = mapped_column(DateTime, default=agora)
    fim: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    kwh: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="ativa")
    validacao: Mapped[str] = mapped_column(String(20), default="valida")

    usuario: Mapped[Usuario] = relationship(back_populates="sessoes")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()