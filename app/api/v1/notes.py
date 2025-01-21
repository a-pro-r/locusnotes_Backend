from fastapi import APIRouter, HTTPException, status
from app.models.notes import Note
from app.services.notes import NoteService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

router = APIRouter(tags=["notes"])


@router.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, db: AsyncSession = Depends(get_db)):
    note_id = await NoteService.create_note(db, note)
    return {"id": note_id, "message": "Note created successfully"}


@router.get("/notes/{note_id}")
async def get_note(note_id: str, db: AsyncSession = Depends(get_db)):
    return await NoteService.get_note(db,note_id)

@router.get("/notes/user/{user_id}") # get all note for a user
async def get_user_notes(user_id: str, db: AsyncSession = Depends(get_db)):
    return await NoteService.get_user_notes(db,user_id)


@router.put("/notes/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(note_id: str,note: Note,db: AsyncSession = Depends(get_db)):
    try:
        # note.user_id would be provided in the Note model from the mobile device
        await NoteService.update_note(note_id, note.user_id, note, db)
        return {"id": note_id, "message": "Note updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or you don't have permission to update it"
        )


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str,user_id: str,db: AsyncSession = Depends(get_db)):
    try:
        await NoteService.delete_note(note_id, user_id, db)
        return None
    except Exception as e:
        if "not found or unauthorized" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or you don't have permission to delete it"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note"
        )
