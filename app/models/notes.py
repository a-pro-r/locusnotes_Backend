from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Note(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    tags: List[str] = []
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    boundary_radius: float = 3218.69  # 2 miles in meters
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True