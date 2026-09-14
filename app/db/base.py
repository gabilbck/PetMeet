"""Base declarativa do SQLAlchemy. Todos os modelos herdam de Base."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
