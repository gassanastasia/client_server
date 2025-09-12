from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Dict

from src.core.models.request import Request
from requests.schemas import RequestCreate

class RequestCRUD:
    async def create(self, session: AsyncSession, request_in: RequestCreate) -> Request:
        db_request = Request(**request_in.dict())
        session.add(db_request)
        await session.flush()
        await session.refresh(db_request)
        return db_request
    
    async def get_all(
        self, 
        session: AsyncSession, 
        page: int = 1, 
        per_page: int = 10
    ) -> Dict:
        offset = (page - 1) * per_page
        
        # Get total count
        total_query = select(func.count()).select_from(Request)
        total_result = await session.execute(total_query)
        total = total_result.scalar()
        
        # Get paginated results
        requests_query = (
            select(Request)
            .order_by(desc(Request.created_at))
            .offset(offset)
            .limit(per_page)
        )
        
        requests_result = await session.execute(requests_query)
        requests = requests_result.scalars().all()
        
        return {
            "items": requests,
            "total": total,
            "page": page,
            "pages": (total + per_page - 1) // per_page if total > 0 else 1,
            "per_page": per_page
        }
    
    async def get_by_id(self, session: AsyncSession, request_id: int) -> Request:
        result = await session.execute(select(Request).filter(Request.id == request_id))
        return result.scalar_one_or_none()

# Global CRUD instance
request_crud = RequestCRUD()