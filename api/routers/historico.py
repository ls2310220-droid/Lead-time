from fastapi import APIRouter
from api.services import historico as svc

router = APIRouter()

@router.get("/{carregamento_id}")
def listar(carregamento_id: int):
    return svc.listar(carregamento_id)
