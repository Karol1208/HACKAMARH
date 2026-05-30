import mysql.connector
from mysql.connector import Error

try:
    # 1. Configurar a conexão com os mesmos dados do Workbench
    conexao = mysql.connector.connect(
        host='localhost',        # Ou o IP do seu servidor
        database='seu_banco',    # Nome do banco de dados
        user='root',             # Seu usuário do MySQL
        password='sua_senha'     # Sua senha do MySQL
    )

    if conexao.is_connected():
        print("Conexão estabelecida com sucesso!")
        
        cursor = conexao.cursor()
        
        cursor.execute("SELECT VERSION();")
        
        linha = cursor.fetchone()
        print(f"Versão do MySQL: {linha[0]}")

except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão com o MySQL encerrada.")