from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.db.client import get_db
from datetime import datetime

router = APIRouter()

class AIRequest(BaseModel):
    pergunta: str
    semana: Optional[int] = None

def _calcular_lead_time(row: dict) -> Optional[int]:
    """Calcula lead time em minutos entre sep e lib"""
    try:
        if row.get("sep") and row.get("lib"):
            for fmt in ["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]:
                try:
                    sep = datetime.strptime(row["sep"], fmt)
                    lib = datetime.strptime(row["lib"], fmt)
                    return int((lib - sep).total_seconds() / 60)
                except:
                    continue
    except:
        pass
    return None

def _calcular_status(row: dict) -> str:
    if row.get("lib"):         return "LIBERADO"
    if row.get("nf"):          return "AGUARDANDO FATURAMENTO"
    if row.get("saiu"):        return "TEMPERATURA/LIBERAÇÃO"
    if row.get("enc"):         return "SAIU DA DOCA"
    if row.get("cheg"):        return "AGUARDANDO ENCOSTAR NA DOCA"
    if row.get("aval"):        return "CARREGANDO"
    if row.get("sep"):         return "AGUARDANDO QUALIDADE"
    if row.get("oe"):          return "AGUARDANDO SEPARAÇÃO"
    if row.get("pv"):          return "AGUARDANDO OE"
    return "AGUARDANDO PV"

def _montar_contexto(carregamentos: list, semana: Optional[int]) -> str:
    if not carregamentos:
        return "Nenhum carregamento encontrado para esta semana."

    total = len(carregamentos)
    liberados = [c for c in carregamentos if c.get("lib")]
    em_andamento = [c for c in carregamentos if not c.get("lib")]
    ag_pv = [c for c in carregamentos if not c.get("pv")]

    lts = [_calcular_lead_time(c) for c in liberados]
    lts = [lt for lt in lts if lt is not None]
    lt_medio = f"{int(sum(lts)/len(lts)//60)}h{int(sum(lts)/len(lts)%60):02d}min" if lts else "N/A"

    # Atrasos: lead time > 480 min (8h)
    atrasados = [c for c in carregamentos if (_calcular_lead_time(c) or 0) > 480]

    linhas = [
        f"SEMANA: {semana or 'atual'}",
        f"TOTAL DE CARREGAMENTOS: {total}",
        f"LIBERADOS: {len(liberados)}",
        f"EM ANDAMENTO: {len(em_andamento)}",
        f"AGUARDANDO PV: {len(ag_pv)}",
        f"LEAD TIME MÉDIO: {lt_medio} (meta: 4h)",
        f"ATRASADOS (LT > 8h): {len(atrasados)}",
        "",
        "DETALHES POR CARREGAMENTO:"
    ]

    for c in carregamentos:
        lt = _calcular_lead_time(c)
        lt_str = f"{lt//60}h{lt%60:02d}min" if lt else "em andamento"
        status = _calcular_status(c)
        linha = (
            f"- Cliente: {c.get('cliente','?')} | "
            f"Pallets: {c.get('pallets','?')} | "
            f"Local: {c.get('local','?')} | "
            f"Status: {status} | "
            f"Lead Time: {lt_str}"
        )
        if c.get("obs"):
            linha += f" | Obs: {c['obs']}"
        linhas.append(linha)

    return "\n".join(linhas)

@router.post("/")
async def analisar(req: AIRequest):
    try:
        import httpx, os

        db = get_db()
        q = db.table("carregamentos").select("*").order("id")
        if req.semana:
            q = q.eq("semana", req.semana)
        res = q.execute()
        carregamentos = res.data or []

        contexto = _montar_contexto(carregamentos, req.semana)

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            # Fallback sem IA: resposta baseada nos dados
            return {"resposta": _resposta_simples(req.pergunta, carregamentos)}

        prompt = f"""Você é um assistente especializado em logística e expedição de cargas.
Analise os dados abaixo e responda à pergunta do usuário de forma objetiva e direta.
Use bullet points quando listar itens. Seja conciso.

DADOS DA OPERAÇÃO:
{contexto}

PERGUNTA: {req.pergunta}"""

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 600,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            data = response.json()
            resposta = data["content"][0]["text"]
            return {"resposta": resposta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _resposta_simples(pergunta: str, carregamentos: list) -> str:
    """Resposta básica sem IA quando não há API key"""
    total = len(carregamentos)
    liberados = len([c for c in carregamentos if c.get("lib")])
    ag_pv = len([c for c in carregamentos if not c.get("pv")])
    atrasados = len([c for c in carregamentos if (_calcular_lead_time(c) or 0) > 480])

    lts = [_calcular_lead_time(c) for c in carregamentos if c.get("lib")]
    lts = [lt for lt in lts if lt is not None]
    lt_medio = f"{int(sum(lts)/len(lts)//60)}h{int(sum(lts)/len(lts)%60):02d}min" if lts else "N/A"

    return (
        f"📊 Resumo da operação:\n"
        f"• Total de carregamentos: {total}\n"
        f"• Liberados: {liberados}\n"
        f"• Em andamento: {total - liberados}\n"
        f"• Aguardando PV: {ag_pv}\n"
        f"• Atrasados (LT > 8h): {atrasados}\n"
        f"• Lead time médio: {lt_medio}\n\n"
        f"Para análises mais detalhadas, configure a variável ANTHROPIC_API_KEY na Vercel."
    )
