from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import os

router = APIRouter()

class AIPergunta(BaseModel):
    pergunta: str
    contexto: str = ""
    semana: int = 0

@router.post("/chat")
async def chat(body: AIPergunta):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"resposta": "⚠ Chave da IA não configurada no servidor."}
    system_prompt = f"""Você é especialista em logística e expedição de frutas.
Dados da semana {body.semana}:
{body.contexto}
Meta: ≤4h. Crítico: >8h."""
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-haiku-4-5-20251001", "max_tokens": 1000, "system": system_prompt, "messages": [{"role": "user", "content": body.pergunta}]},
            timeout=30.0
        )
        d = res.json()
        return {"resposta": d.get("content", [{}])[0].get("text", "Sem resposta.")}
