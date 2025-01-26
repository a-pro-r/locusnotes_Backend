from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.users import UserService
from pydantic import EmailStr

router = APIRouter(tags=["users"])

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(email: EmailStr, db: AsyncSession = Depends(get_db)):
    try:
        user_id = await UserService.register_user(db, email)
        return {"id": user_id, "email": email}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )