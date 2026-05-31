import os
import psycopg2
from psycopg2.extras import RealDictCursor


class Conexao:
    def __init__(self):
        self._conn = psycopg2.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME', 'hackamarh'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD')
        )

    def cursor(self):
        return self._conn.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        self._conn.commit()

    def fechar(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        if exc_type:
            self._conn.rollback()
        else:
            self._conn.commit()
        self.fechar()
