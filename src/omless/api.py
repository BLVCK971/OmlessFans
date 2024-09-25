from fastapi import APIRouter

from omless.modules.video.endpoints import router as video_router

api_router = APIRouter()

@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}

api_router.include_router(video_router, prefix="/video", tags=["Vidéo"])

