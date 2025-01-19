from app.models.notes import Note
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
import json
from app.db.models import NoteDB
import uuid

class NoteService:
    @staticmethod
    async def create_note(session: AsyncSession, note: Note) -> str:
        try:
            # Create new note instance
            db_note = NoteDB(
                id=uuid.uuid4(),
                user_id=uuid.UUID(note.user_id),
                title=note.title,
                content=note.content,
                tags=json.dumps(note.tags),
                location_name=note.location_name,
                address=note.address
            )
            # Create Location point
            if note.latitude is not None and note.longitude is not None:
                point = Point(note.longitude, note.latitude)
                db_note.location = from_shape(point, srid=4326)

            # Add to database
            session.add(db_note)
            await session.commit()
            await session.refresh(db_note)

            return str(db_note.id)

        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to create note: {str(e)}")


    @staticmethod
    async def get_note(note_id: str) -> Note:
        # Implementation for getting note
        pass

    @staticmethod
    async def update_note(note_id: str, note: Note):
        # Implementation for updating note
        pass

    @staticmethod
    async def delete_note(note_id: str):
        # Implementation for deleting note
        pass
