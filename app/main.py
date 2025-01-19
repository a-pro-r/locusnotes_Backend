from fastapi import FastAPI
from mangum import Mangum
from app.api.v1 import notes, location
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    root_path="/prod"  # For API Gateway stage
)

# Include routers
app.include_router(notes.router, prefix=settings.API_V1_STR)
app.include_router(location.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# AWS Lambda handler
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)