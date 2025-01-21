from sqlalchemy import select, delete
from app.models.notes import Note
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from sqlalchemy import and_
from datetime import datetime
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
                tags=note.tags,
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
    async def get_note(session: AsyncSession, note_id: str) -> dict:
        try:

            stmt = select(NoteDB).where(NoteDB.id == note_id)


            result = await session.execute(stmt)
            db_note = result.scalar_one_or_none()

            if db_note is None:
                raise Exception(f"Note with id {note_id} not found")


            lat, lon = None, None
            if db_note.location is not None:
                # Convert PostGIS point to shapely point
                point = to_shape(db_note.location)
                lat = point.y
                lon = point.x

            return {
                "id": str(db_note.id),  # Keep as string for JSON
                "user_id": str(db_note.user_id),
                "title": db_note.title,
                "content": db_note.content,
                "tags": db_note.tags,
                "location_name": db_note.location_name,
                "latitude": lat,
                "longitude": lon,
                "address": db_note.address,
                "created_at": db_note.created_at.isoformat(),  # Convert datetime to string
                "updated_at": db_note.updated_at.isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to retrieve note: {str(e)}")


    @staticmethod
    async def update_note(note_id: str, user_id: str, note: Note, session: AsyncSession):
        try:
            stmt = select(NoteDB).where(
                and_(
                    NoteDB.id == note_id,
                    NoteDB.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            db_note = result.scalar_one_or_none()

            if db_note is None:
                raise Exception(f"Note with id {note_id} not found")

            # update lat lon -> location
            if note.latitude is not None and note.longitude is not None:
                point = Point(note.longitude, note.latitude)
                db_note.location = from_shape(point, srid=4326)
                db_note.location_name = note.location_name
                db_note.address = note.address
            else:
                db_note.location = None
                db_note.location_name = None
                db_note.address = None

            db_note.title = note.title
            db_note.content = note.content
            db_note.tags = note.tags
            db_note.updated_at = datetime.utcnow()

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to update note: {str(e)}")



    @staticmethod
    async def delete_note(note_id: str, user_id: str, session: AsyncSession):
        try:
            stmt = delete(NoteDB).where(
                and_(
                    NoteDB.id == note_id,
                    NoteDB.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise Exception("Note not found or unauthorized")

            await  session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to delete note: {str(e)}")


    @staticmethod
    async def get_user_notes(session: AsyncSession, user_id: str) -> list[dict]:
        try:

            stmt = select(NoteDB).where(NoteDB.user_id == user_id)

            result = await session.execute(stmt)
            db_notes =  result.scalars().all()  # Fetch all notes as a list
            if db_notes is None:
                raise Exception(f"Notes for userID: {user_id} not found")
            notes = []
            for db_note in db_notes:
                lat, lon = None, None
                if db_note.location is not None:
                    # Convert PostGIS point to shapely point
                    point = to_shape(db_note.location)
                    lat = point.y
                    lon = point.x

                note = {
                    "id": str(db_note.id),  # Keep as string for JSON
                    "user_id": str(db_note.user_id),
                    "title": db_note.title,
                    "content": db_note.content,
                    "tags": db_note.tags,
                    "location_name": db_note.location_name,
                    "latitude": lat,
                    "longitude": lon,
                    "address": db_note.address,
                    "created_at": db_note.created_at.isoformat(),  # Convert datetime to string
                    "updated_at": db_note.updated_at.isoformat()
                }
                notes.append(note)
            return notes

        except Exception as e:
            raise Exception(f"Failed to retrieve note: {str(e)}")
