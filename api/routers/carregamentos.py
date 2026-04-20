from fastapi import APIRouter
from api.services import carregamentos as svc
from api.models.schemas import CarregamentoCreate, CarregamentoUpdate, MotivoUpdate, ObsUpdate

router = APIRouter()

@router.get("")
def listar(semana: int = None):
    return svc.listar(semana)

@router.get("/{id}")
def buscar(id: int):
    return svc.buscar(id)

@router.post("")
def criar(body: CarregamentoCreate):
    return svc.criar(body)

@router.patch("/{id}/campo")
def atualizar_campo(id: int, body: CarregamentoUpdate):
    return svc.atualizar_campo(id, body.field, body.value)

@router.patch("/{id}/motivo")
def atualizar_com_motivo(id: int, body: MotivoUpdate):
    return svc.atualizar_com_motivo(id, body.field, body.value, body.motivo)

@router.patch("/{id}/obs")
def atualizar_obs(id: int, body: ObsUpdate):
    return svc.atualizar_obs(id, body.obs)

@router.delete("/{id}")
def deletar(id: int):
    return svc.deletar(id)
