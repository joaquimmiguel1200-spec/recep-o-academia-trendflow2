from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import StudentModel
from app.schemas import AccessStatus

class AccessControlService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_access(self, student_id: int) -> tuple[AccessStatus, StudentModel | None]:
        result = await self.db.execute(select(StudentModel).filter(StudentModel.id == student_id))
        student = result.scalar_one_or_none()

        if not student:
            return AccessStatus.BLOCKED, None
        
        if not student.is_active:
            return AccessStatus.INACTIVE_PLAN, student
        
        if student.financial_due_date < datetime.now():
            return AccessStatus.EXPIRED_PAYMENT, student
            
        return AccessStatus.GRANTED, student