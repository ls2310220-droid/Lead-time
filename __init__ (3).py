from api.db.client import get_db
from fastapi import HTTPException

CAMPOS_PERMITIDOS = ['pv','oe','sep','aval','cheg','enc','saiu','nf','lib','draft_dt','draft_tipo']

def listar(semana: int = None):
    db = get_db()
    q = db.table("carregamentos").select("*").order("id")
    if semana:
        q = q.eq("semana", semana)
    res = q.execute()
    return res.data

def buscar(id: int):
    db = get_db()
    res = db.table("carregamentos").select("*").eq("id", id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Carregamento não encontrado")
    return res.data

def criar(body):
    db = get_db()
    payload = body.model_dump()
    res = db.table("carregamentos").insert(payload).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Erro ao criar carregamento")
    novo = res.data[0]
    _add_historico(novo["id"], "📦 CRIADO", f"Carregamento de {body.cliente} registrado para semana {body.semana}")
    return novo

def atualizar_campo(id: int, field: str, value: str):
    if field not in CAMPOS_PERMITIDOS:
        raise HTTPException(status_code=400, detail=f"Campo '{field}' não permitido")
    db = get_db()
    row = buscar(id)
    old_value = row.get(field, "")
    res = db.table("carregamentos").update({field: value}).eq("id", id).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Erro ao atualizar")
    _add_historico(id, f"✏ EDIÇÃO", f"Campo '{field}' alterado: '{old_value}' → '{value}'")
    return res.data[0]

def atualizar_com_motivo(id: int, field: str, value: str, motivo: str):
    if field not in CAMPOS_PERMITIDOS:
        raise HTTPException(status_code=400, detail=f"Campo '{field}' não permitido")
    db = get_db()
    buscar(id)
    res = db.table("carregamentos").update({field: value, "motivo_status": motivo}).eq("id", id).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Erro ao atualizar")
    _add_historico(id, "🚛 SEM PV", f"Campo '{field}' preenchido sem PV. Motivo: {motivo}", value)
    return res.data[0]

def atualizar_obs(id: int, obs: str):
    db = get_db()
    buscar(id)
    res = db.table("carregamentos").update({"obs": obs}).eq("id", id).execute()
    return res.data[0]

def deletar(id: int):
    db = get_db()
    buscar(id)
    db.table("historico_carregamento").delete().eq("carregamento_id", id).execute()
    db.table("carregamentos").delete().eq("id", id).execute()
    return {"ok": True, "id": id}

def _add_historico(carregamento_id: int, tipo: str, descricao: str, extra: str = ""):
    from datetime import datetime
    db = get_db()
    now = datetime.now()
    dt_str = f"{now.day:02d}/{now.month:02d}/{now.year} {now.hour:02d}:{now.minute:02d}"
    db.table("historico_carregamento").insert({
        "carregamento_id": carregamento_id,
        "dt": dt_str,
        "tipo": tipo,
        "descricao": descricao,
        "extra": extra
    }).execute()
