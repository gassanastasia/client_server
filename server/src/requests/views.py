from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from requests.schemas import RequestCreate, RequestResponse, RequestList
from requests.crud import request_crud

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.post(
    "", 
    response_model=RequestResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new request"
)
async def create_request(
    request: RequestCreate,
    session: AsyncSession = Depends(db_helper.get_session)
):
    """
    Create a new request with text, date, time and click count.
    """
    try:
        return await request_crud.create(session, request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create request: {str(e)}"
        )

@router.get(
    "",
    response_model=RequestList,
    summary="Get paginated list of requests"
)
async def get_requests(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(db_helper.get_session)
):
    """
    Retrieve paginated list of all requests.
    """
    try:
        return await request_crud.get_all(session, page, per_page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch requests: {str(e)}"
        )