from abc import ABC, abstractmethod
from typing import Protocol
from app.schemas import AccessStatus
import structlog

logger = structlog.get_logger()

class GateController(Protocol):
    """Protocolo para integração com hardware (Catracas, Biometria)"""
    async def release_gate(self, device_id: str) -> bool: ...
    async def block_gate(self, device_id: str, message: str) -> bool: ...

class BaseHardwareIntegration(ABC):
    @abstractmethod
    async def process_entry(self, identifier: str) -> AccessStatus:
        pass

class MockGateController:
    async def release_gate(self, device_id: str) -> bool:
        logger.info("hardware_event", action="release", device=device_id)
        return True

    async def block_gate(self, device_id: str, message: str) -> bool:
        logger.error("hardware_event", action="block", device=device_id, reason=message)
        return True