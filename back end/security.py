import os
import time
from collections import defaultdict
from fastapi import Header, HTTPException, Request, status

# ── Chave de Admin ────────────────────────────────────────────────────────────
# Em produção: defina ADMIN_SECRET_KEY no ambiente
_ADMIN_KEY = os.getenv('ADMIN_SECRET_KEY', '')

def verificar_chave_admin(x_admin_key: str = Header(..., alias='X-Admin-Key')):
    if not _ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticação não configurada. Defina ADMIN_SECRET_KEY no servidor."
        )
    if x_admin_key != _ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )

# ── Rate Limiter em memória ───────────────────────────────────────────────────
# Limita endpoints pesados (ML/upload) a 10 req/min por IP
_rate_store: dict[str, list[float]] = defaultdict(list)
_JANELA_SEG = 60
_MAX_REQUISICOES = 10

def verificar_rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    agora = time.time()
    hits = [t for t in _rate_store[ip] if agora - t < _JANELA_SEG]
    if len(hits) >= _MAX_REQUISICOES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Muitas requisições. Aguarde {_JANELA_SEG} segundos."
        )
    hits.append(agora)
    _rate_store[ip] = hits
