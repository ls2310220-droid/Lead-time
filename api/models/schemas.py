from pydantic import BaseModel
from typing import Optional

class CarregamentoCreate(BaseModel):
    cliente: str
    pallets: Optional[int] = None
    local: str = "FLK"
    semana: int
    draft_dt: Optional[str] = ""
    draft_tipo: Optional[str] = ""
    pv: Optional[str] = ""
    oe: Optional[str] = ""
    sep: Optional[str] = ""
    aval: Optional[str] = ""
    cheg: Optional[str] = ""
    enc: Optional[str] = ""
    saiu: Optional[str] = ""
    nf: Optional[str] = ""
    lib: Optional[str] = ""
    obs: Optional[str] = ""

class CarregamentoUpdate(BaseModel):
    field: str
    value: str

class MotivoUpdate(BaseModel):
    field: str
    value: str
    motivo: str

class ObsUpdate(BaseModel):
    obs: str

class HistoricoCreate(BaseModel):
    dt: str
    tipo: str
    descricao: str
    extra: Optional[str] = ""

class CarregamentoOut(BaseModel):
    id: int
    cliente: str
    pallets: Optional[int]
    local: str
    semana: int
    draft_dt: Optional[str]
    draft_tipo: Optional[str]
    pv: Optional[str]
    oe: Optional[str]
    sep: Optional[str]
    aval: Optional[str]
    cheg: Optional[str]
    enc: Optional[str]
    saiu: Optional[str]
    nf: Optional[str]
    lib: Optional[str]
    obs: Optional[str]
    motivo_status: Optional[str]

class HistoricoOut(BaseModel):
    id: int
    carregamento_id: int
    dt: str
    tipo: str
    descricao: str
    extra: Optional[str]
