<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from psycopg2.extras import RealDictCursor
from connection import Conexao  # Importa a classe do seu arquivo connection.py
import schemas  # Importa os esquemas de validação do Pydantic

router = APIRouter(prefix="/users", tags=["users"])

def get_conexao():
    """Retorna uma nova instância de gerenciamento da conexão com o banco."""
    return Conexao()


# ==========================================
# 1. ROTAS DE USUÁRIOS (MÓDULO GOV / ADMIN)
# ==========================================

@router.post("/", response_model=schemas.UsuarioResposta, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCriar):
    with get_conexao() as conn:
        with conn.cursor() as cursor:
            # Verifica se o usuário já existe
            cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (usuario.email,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="E-mail já cadastrado."
                )
            
            # Insere o novo usuário interno
            query = """
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (%s, %s, %s)
                RETURNING id, nome, email, created_at AS criado_em;
            """
            cursor.execute(query, (usuario.nome, usuario.email, usuario.senha))
            novo_usuario = cursor.fetchone()
            
    return novo_usuario
=======
from fastapi import APIRouter, HTTPException
from connection import Conexao
import schemas
>>>>>>> b8bdefc0dd1eaf03f933f3143f62dd14600b0838


@router.get("/", response_model=list[schemas.UsuarioResposta])
def listar_usuarios():
<<<<<<< HEAD
    with get_conexao() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, email, created_at AS criado_em FROM usuarios;")
            usuarios = cursor.fetchall()
    return usuarios


# ==========================================
# 2. ROTAS DOS PRODUTORES (APP CANINDÉ)
# ==========================================

@router.post("/produtores", response_model=schemas.UsuarioProdutorResposta, status_code=status.HTTP_201_CREATED)
def criar_produtor(produtor: schemas.UsuarioProdutorCriar):
    with get_conexao() as conn:
        with conn.cursor() as cursor:
            # Verifica se o ID do Firebase ou o CAR já existem
            cursor.execute("SELECT id FROM usuarios_produtores WHERE id = %s OR numero_car = %s;", (produtor.id, produtor.numero_car))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Produtor ou número de CAR já cadastrado."
                )
            
            # Insere os dados vindos do Flutter offline-first
            query = """
                INSERT INTO usuarios_produtores (id, nome, numero_car, device_token, status_prad)
                VALUES (%s, %s, %s, %s, 'em_dia')
                RETURNING id, nome, numero_car, device_token, status_prad, created_at;
            """
            cursor.execute(query, (produtor.id, produtor.nome, produtor.numero_car, produtor.device_token))
            novo_produtor = cursor.fetchone()
            
    return novo_produtor


@router.get("/produtores/{produtor_id}", response_model=schemas.UsuarioProdutorResposta)
def obter_produtor(produtor_id: str):
    with get_conexao() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, numero_car, device_token, status_prad, created_at FROM usuarios_produtores WHERE id = %s;", (produtor_id,))
            produtor = cursor.fetchone()
            
            if not produtor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Produtor não encontrado."
                )
    return produtor


@router.put("/produtores/{produtor_id}", response_model=schemas.UsuarioProdutorResposta)
def atualizar_produtor(produtor_id: str, dados: schemas.UsuarioProdutorAtualizar):
    with get_conexao() as conn:
        with conn.cursor() as cursor:
            # Verifica se o registro existe
            cursor.execute("SELECT * FROM usuarios_produtores WHERE id = %s;", (produtor_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor não encontrado.")
            
            # Monta a query dinamicamente conforme os campos preenchidos
            campos = []
            valores = []
            
            if dados.nome is not None:
                campos.append("nome = %s")
                valores.append(dados.nome)
            if dados.numero_car is not None:
                campos.append("numero_car = %s")
                valores.append(dados.numero_car)
            if dados.status_prad is not None:
                campos.append("status_prad = %s")
                valores.append(dados.status_prad)
            if dados.device_token is not None:
                campos.append("device_token = %s")
                valores.append(dados.device_token)
                
            if not campos:
                raise HTTPException(status_code=400, detail="Nenhum campo para atualizar foi fornecido.")
                
            valores.append(produtor_id)
            query = f"""
                UPDATE usuarios_produtores 
                SET {', '.join(campos)} 
                WHERE id = %s
                RETURNING id, nome, numero_car, device_token, status_prad, created_at;
            """
            cursor.execute(query, tuple(valores))
            produtor_atualizado = cursor.fetchone()
            
    return produtor_atualizado
=======
    with Conexao() as db:
        cur = db.cursor()
        cur.execute("SELECT id, nome, email, criado_em FROM usuarios")
        return cur.fetchall()

@router.get("/{usuario_id}", response_model=schemas.UsuarioResposta)
def buscar_usuario(usuario_id: int):
    with Conexao() as db:
        cur = db.cursor()
        cur.execute("SELECT id, nome, email, criado_em FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cur.fetchone()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/", response_model=schemas.UsuarioResposta, status_code=201)
def criar_usuario(dados: schemas.UsuarioCriar):
    with Conexao() as db:
        cur = db.cursor()
        cur.execute("SELECT id FROM usuarios WHERE email = %s", (dados.email,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        cur.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id, nome, email, criado_em",
            (dados.nome, dados.email, dados.senha),
        )
        return cur.fetchone()

@router.patch("/{usuario_id}", response_model=schemas.UsuarioResposta)
def atualizar_usuario(usuario_id: int, dados: schemas.UsuarioAtualizar):
    with Conexao() as db:
        cur = db.cursor()
        cur.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        campos = dados.model_dump(exclude_none=True)
        if campos:
            set_clause = ", ".join(f"{c} = %s" for c in campos)
            cur.execute(
                f"UPDATE usuarios SET {set_clause} WHERE id = %s RETURNING id, nome, email, criado_em",
                (*campos.values(), usuario_id),
            )
            return cur.fetchone()
        cur.execute("SELECT id, nome, email, criado_em FROM usuarios WHERE id = %s", (usuario_id,))
        return cur.fetchone()

@router.delete("/{usuario_id}", status_code=204)
def deletar_usuario(usuario_id: int):
    with Conexao() as db:
        cur = db.cursor()
        cur.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
>>>>>>> b8bdefc0dd1eaf03f933f3143f62dd14600b0838
