from options_reticle.paths import DATABASE_LOCATION
from options_reticle.models import Base, SymbolsTable, ExpirationsTable

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from more_itertools import flatten

from loguru import logger

database_uri = f"sqlite:////{DATABASE_LOCATION}"


class DatabaseConnection:
    Session = None

    @staticmethod
    def create_session():
        engine = create_engine(database_uri)
        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine)

    @classmethod
    @contextmanager
    def session_manager(cls):

        if cls.Session is None:
            cls.Session = cls.create_session()

        session = cls.Session()

        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(e)
            raise e
        finally:
            session.close()


class SymbolsDatabase(DatabaseConnection):
    Session = None
    table = SymbolsTable

    @classmethod
    def add_symbol(cls, symbol, exchange):
        with cls.session_manager() as session:
            symbol = cls.table(symbol=symbol, exchange=exchange)

            try:
                session.add(symbol)
                session.commit()

            except IntegrityError as e:
                session.rollback()

    @classmethod
    def get_all_symbols_without_quotes(cls):
        with cls.session_manager() as session:
            query = session.query(cls.table.symbol).filter(cls.table.close == None).all()
            return sorted(flatten(query))

    @classmethod
    def update_symbols_with_quotes(cls, quote_data):
        with cls.session_manager() as session:
            for symbol, close in quote_data.items():
                query = session.query(cls.table).filter(cls.table.symbol == symbol).first()
                query.close = close
                session.commit()
