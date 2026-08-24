# Python 3.12+
import structlog
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.database import init_db, SessionLocal
from app.schemas import AccessStatus, AccessLog, TenantConfig
from app.services import AccessControlService
from app.hardware_bridge import MockGateController

# Configuração de Logs Estruturados
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="TrendFlow 2 - Gym Reception & Access Control",
    version="2.0.0",
    lifespan=lifespan
)

# Injeção de Dependência do Banco
async def get_db():
    async with SessionLocal() as session:
        yield session

# Configuração Mock do Tenant (Personalização B2B)
GYM_CONFIG = TenantConfig(
    name="TrendFlow Fitness Center",
    primary_color="#FF5733",
    logo_url="https://cdn.trendflow.io/logos/gym_default.png"
)

@app.get("/api/v1/config")
async def get_gym_config() -> TenantConfig:
    """Retorna as configurações de branding da academia"""
    return GYM_CONFIG

@app.post("/api/v1/access/check-in/{student_id}")
async def check_in(
    student_id: int, 
    operator: str = "RECEPTION_01",
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Realiza o controle de acesso e integra com hardware virtual
    """
    service = AccessControlService(db)
    gate = MockGateController()
    
    status, student = await service.validate_access(student_id)
    
    # Simulação de integração com hardware
    if status == AccessStatus.GRANTED:
        await gate.release_gate(device_id="CATRACA_PRINCIPAL")
    else:
        await gate.block_gate(device_id="CATRACA_PRINCIPAL", message=status.value)

    log = AccessLog(
        student_id=student_id,
        status=status,
        responsible_user=operator
    )
    
    logger.info("access_attempt", 
                student=student.full_name if student else "Unknown", 
                status=status.value)

    return {
        "status": status,
        "student_name": student.full_name if student else "NÃO ENCONTRADO",
        "timestamp": log.timestamp,
        "branding": GYM_CONFIG.model_dump()
    }

@app.get("/api/v1/dashboard/summary")
async def get_dashboard_summary():
    """Indicadores rápidos para a recepção"""
    # Mock de dados agregados para exemplo
    return {
        "present_now": 42,
        "daily_entries": 156,
        "pending_payments": 5,
        "expiring_soon": 12,
        "alerts": [
            {"type": "FINANCIAL", "msg": "3 alunos com mais de 10 dias de atraso"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)