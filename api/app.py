from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core.config import settings
from core.logger import logger
from core.exceptions import DentovisionException
from inference.yolo_detector import YOLODetector

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application.
    Initializes heavy resources (like ML models) before the app starts accepting requests.
    """
    logger.info("Initializing YOLOv8 detector on startup...")
    app.state.detector = YOLODetector()
    yield
    logger.info("Shutting down and cleaning up resources...")
    app.state.detector = None

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router, tags=["Predictions"])
    
    # Global exception handler
    @app.exception_handler(DentovisionException)
    async def dentovision_exception_handler(request: Request, exc: DentovisionException):
        logger.error(f"Handled custom exception: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={"error": exc.message}
        )
        
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": "An internal server error occurred."}
        )

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "environment": settings.environment}

    return app

app = create_app()
