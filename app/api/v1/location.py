from fastapi import APIRouter, HTTPException
from typing import List
from app.services.location import LocationService

router = APIRouter(tags=["location"])

@router.post("/location/update")
async def update_location(latitude: float, longitude: float):
    await LocationService.update_location(latitude, longitude)
    return {"message": "Location updated successfully"}

@router.get("/location/nearby")
async def get_nearby_notes(radius: float = 3218.69):  # Default 2 miles
    notes = await LocationService.get_nearby_notes(radius)
    return notes