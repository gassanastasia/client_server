from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .core.db_helper import db_helper
from .requests import router as requests_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting server application...")
    await db_helper.create_tables()
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down server...")
    await db_helper.dispose()
    logger.info("Database disposed")

app = FastAPI(
    title="Request Server API",
    description="API for handling client requests",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(requests_router)

@app.get("/")
async def root():
    return {"message": "Request Server API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port,
        reload=True
    )