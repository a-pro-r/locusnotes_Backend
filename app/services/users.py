from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserDB
from app.models.users import User
from sqlalchemy import select
import uuid


class UserService:
    @staticmethod
    async def register_user(session: AsyncSession, email: str) -> str:
        try:
            # Check if user exists
            stmt = select(UserDB).where(UserDB.email == email)
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                return str(existing_user.id)

            # Create new user
            db_user = UserDB(
                id=uuid.uuid4(),
                email=email
            )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

            return str(db_user.id)

        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to register user: {str(e)}")