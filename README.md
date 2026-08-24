# TrendFlow 2 - Gym Management System

## Arquitetura
- **FastAPI**: Backend de alta performance.
- **SQLAlchemy 2.0**: ORM Assíncrono para operações de banco.
- **Pydantic v2**: Validação de dados e schemas.
- **Hardware Bridge**: Camada de abstração via Protocolos/Interfaces para facilitar integração futura com SDKs de fabricantes (TopData, Control iD, Henry).

## Como executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute a aplicação: `python main.py`
3. Acesse a documentação Swagger: `http://localhost:8000/docs`

## Customização (Multi-tenant)
O endpoint `/api/v1/config` fornece as definições de UI (cores, logo) que o frontend deve consumir para aplicar o branding da unidade específica.