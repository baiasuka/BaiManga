from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import config


class DB_Connection:
    def __init__(self, host=None, port=None, username=None, password=None, db_name=None):
        self.host = host if host else config.HOST
        self.port = port if port else config.PORT
        self.username = username if username else config.USERNAME
        self.password = password if password else config.PASSWORD
        self.dbs = db_name if db_name else config.DATABASE
        self.dialect = config.DIALECT
        self.driver = config.DRIVER

        self.engine = self.get_engine()

    def get_engine(self):
        # print(self.dbs)
        return create_engine('{dialect}+{driver}://{username}:{password}@{host}:{port}/{dbs}'.format(
            dialect=self.dialect,
            driver=self.driver, username=self.username, password=self.password, host=self.host, port=self.port,
            dbs=self.dbs))

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session

    @contextmanager
    def open_session(self):
        """
        可以使用 with 上下文，在 with 结束之后自动 commit
        """
        Session = self.get_session()
        _session = Session()
        try:
            yield _session
            _session.commit()
        except Exception as e:
            # _session.rollback()
            raise e
        finally:
            _session.close()

    def excute_query(self, sql, params=None):
        with self.open_session() as session:
            try:
                result = session.execute(text(sql), params).fetchall()
            except Exception as e:
                session.rollback()
            else:
                return result

    def excute_update(self, sql, params):
        with self.open_session() as session:
            try:
                session.execute(text(sql), params)
                # print("excuted")
            except Exception as e:
                print(e)
                session.rollback()
            else:
                return True

    def excute_delete(self, sql, params):
        with self.open_session() as session:
            try:
                session.execute(text(sql), params)
            except Exception as e:
                session.rollback()
            else:
                return True
