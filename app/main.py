"""
this is the main entry point for the FastAPI application.
"""
from fastapi import FastAPI
# from app.core.config import settings

app = FastAPI(
    title="MindForge - A place to forge new skills and knowledge",
    description="A comprehensive platform for managing learning resources,\
        courses, and user interactions.",
)

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to MindForge - A place to forge new skills and knowledge!"}
