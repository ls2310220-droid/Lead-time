from fastapi import APIRouter
from api.services import carregamentos as svc

router = APIRouter()

@router.get("")
def dashboard(semana: int = None):
    dados = svc.listar(semana)
    total = len(dados)
    concluidos = sum(1 for d in dados if d.get("saiu"))
    criticos = sum(1 for d in dados if not d.get("pv"))
    return {
        "total": total,
        "concluidos": concluidos,
        "criticos": criticos,
        "pendentes": total - concluidos
    }
