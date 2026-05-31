from fastapi import APIRouter, HTTPException
from connection import Conexao
import schemas

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=list[schemas.UsuarioResposta])
def listar_usuarios():
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
