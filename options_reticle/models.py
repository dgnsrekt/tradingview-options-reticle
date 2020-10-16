from sqlalchemy import Column, String, DateTime, Integer, BigInteger
from sqlalchemy import UniqueConstraint, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class SymbolsTable(Base):
    __tablename__ = "symbols"

    id = Column(Integer, index=True, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    exchange = Column(String, nullable=False)
    close = Column(Numeric, nullable=True)

    expiration_dates = relationship("ExpirationsTable", backref="symbols", lazy=True)


class ExpirationsTable(Base):
    __tablename__ = "expirations"

    id = Column(Integer, index=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)

    __table_args__ = (UniqueConstraint("date", "symbol_id"),)
