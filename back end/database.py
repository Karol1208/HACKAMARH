import os
import psycopg2
from psycopg2 import Error

conexao = None

try:
    # Ler configuração via variáveis de ambiente (mais seguro)
    host = os.getenv('DB_HOST', '127.0.0.1')
    port = int(os.getenv('DB_PORT', 5432))
    database = os.getenv('DB_NAME', 'hackamarh')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '123456')  # sem valor padrão por segurança

    if not password:
        raise ValueError('DB_PASSWORD ')

    conexao = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    print("Conexão estabelecida com sucesso!")

    with conexao.cursor() as cursor:
        cursor.execute("SELECT version();")
        linha = cursor.fetchone()
        print(f"Versão do PostgreSQL: {linha[0]}")

except (Exception, Error) as error:
    print(f"Erro ao conectar ao PostgreSQL: {error}")

finally:
    if conexao is not None:
        try:
            if getattr(conexao, 'closed', 1) == 0:
                conexao.close()
                print("Conexão com o PostgreSQL encerrada.")
        except Exception:
            pass
