from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Note(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    tags: List[str] = []
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    boundary_radius: float = 3218.69  # 2 miles in meters
    created_at: Optional[datetime] = None # handled by postgres
    updated_at: Optional[datetime] = None # handled by postgres, must send duing note updates

    class Config:
        from_attributes = True