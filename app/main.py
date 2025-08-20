"""
MindForge FastAPI Application
this is the main entry point for the FastAPI application.
"""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import user, auth, course


app = FastAPI(
    title="MindForge - A place to forge new skills and knowledge",
    description="A comprehensive platform for managing learning resources,\
        courses, and user interactions.",
)

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(course.router, prefix="/api/v1/courses", tags=["courses"])

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to MindForge - A place to forge new skills and knowledge!"}


def custom_openapi():
    """Generate custom OpenAPI schema for the application.

    This function modifies the OpenAPI schema to include security definitions
    and global security requirements for JWT authentication.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add global security requirement
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# apply it to the app
app.openapi = custom_openapi
