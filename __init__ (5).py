from api.db.client import get_db
from fastapi import HTTPException

def listar_por_carregamento(carregamento_id: int):
    db = get_db()
    res = db.table("historico_carregamento")\
        .select("*")\
        .eq("carregamento_id", carregamento_id)\
        .order("id")\
        .execute()
    return res.data

def adicionar(carregamento_id: int, body):
    db = get_db()
    res = db.table("historico_carregamento").insert({
        "carregamento_id": carregamento_id,
        "dt": body.dt,
        "tipo": body.tipo,
        "descricao": body.descricao,
        "extra": body.extra or ""
    }).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Erro ao gravar histórico")
    return res.data[0]
