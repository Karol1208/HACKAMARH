from fastapi import APIRouter, HTTPException
from psycopg2.extras import RealDictCursor
from connection import get_conexao
import schemas

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=list[schemas.UsuarioResposta])
def listar_usuarios():
    conn = get_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, nome, email, criado_em FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.UsuarioResposta)
def buscar_usuario(usuario_id: int):
    conn = get_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, nome, email, criado_em FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/", response_model=schemas.UsuarioResposta, status_code=201)
def criar_usuario(dados: schemas.UsuarioCriar):
    conn = get_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (dados.email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id, nome, email, criado_em",
        (dados.nome, dados.email, dados.senha)
    )
    usuario = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return usuario

@router.patch("/{usuario_id}", response_model=schemas.UsuarioResposta)
def atualizar_usuario(usuario_id: int, dados: schemas.UsuarioAtualizar):
    conn = get_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    campos = dados.model_dump(exclude_none=True)
    if campos:
        set_clause = ", ".join(f"{c} = %s" for c in campos)
        cursor.execute(
            f"UPDATE usuarios SET {set_clause} WHERE id = %s RETURNING id, nome, email, criado_em",
            (*campos.values(), usuario_id)
        )
        usuario = cursor.fetchone()
        conn.commit()
    else:
        cursor.execute("SELECT id, nome, email, criado_em FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

@router.delete("/{usuario_id}", status_code=204)
def deletar_usuario(usuario_id: int):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()
