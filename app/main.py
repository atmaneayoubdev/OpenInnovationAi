import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from app.api.endpoints import router as endpoints_router
from app.core.middleware import setup_middleware
from app.core.logging import configure_logger, logger

DOCUMENTS_PATH = os.path.join("app", "documents")
VECTORSTORE_PATH = os.path.join("app", "vectorstore")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Code to run before the app starts handling requests (e.g., loading models)
    print("App is starting... Loading models and resources.")

    # Create necessary directories
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)
    os.makedirs(VECTORSTORE_PATH, exist_ok=True)
    logger.info(
        f"Ensured directories exist: {DOCUMENTS_PATH}, {VECTORSTORE_PATH}")

    yield  # App is running now, handling requests

    # Teardown: Code to run after the app shuts down (e.g., releasing resources)
    print("App is shutting down... Cleaning up resources.")
    # Here you can clean up any resources, if needed (e.g., releasing model, closing DB connections)

# Create FastAPI instance with lifespan context manager
app = FastAPI(
    title="Technical Challenge for Open Innovation AI",
    description="A FastAPI project to demonstrate a document-based RAG system using Llama 2 embeddings.",
    version="1.0.0",
    contact={
        "name": "Atmane Ayoub",
        "email": "atmaneayoub10@gmail.com",
    },
)

configure_logger()
setup_middleware(app)

# Health check endpoint


@app.get("/health-check")
def home():
    return {"Health Check": "OK"}


@app.get("/documents/{filename}")
async def get_document(filename: str):
    file_path = os.path.join("app", "documents", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}

# Include the API endpoints
app.include_router(endpoints_router, prefix="/api/v1")
