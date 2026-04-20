from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import carregamentos, historico, dashboard, ai

app = FastAPI(title="Lead Time API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(carregamentos.router, prefix="/api/carregamentos", tags=["Carregamentos"])
app.include_router(historico.router,     prefix="/api/historico",     tags=["Histórico"])
app.include_router(dashboard.router,     prefix="/api/dashboard",     tags=["Dashboard"])
app.include_router(ai.router,            prefix="/api/ai",            tags=["IA"])

@app.get("/api/health")
def health():
    return {"status": "ok", "sistema": "Lead Time API"}
