from api.db.client import get_db

def listar(carregamento_id: int):
    db = get_db()
    res = db.table("historico_carregamento").select("*").eq("carregamento_id", carregamento_id).order("id").execute()
    return res.data
