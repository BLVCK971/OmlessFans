from fastapi import APIRouter, status, HTTPException
from omless.modules.video.models import VideoBase
import omless.modules.video.service as service

import logging

router = APIRouter()

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s;")


from omless.database.core import DbSession
from omless.database.service import CommonParameters, search_filter_sort_paginate
from omless.models import PrimaryKey

from .models import VideoCreate, VideoPagination, VideoRead, VideoUpdate
from .service import create, delete, get, update

router = APIRouter()


@router.get("", response_model=VideoPagination)
def get_videos(common: CommonParameters):
    """Get all videos."""
    return search_filter_sort_paginate(model="Video", **common)


@router.get("/{video_id}", response_model=VideoRead)
def get_video(db_session: DbSession, video_id: PrimaryKey):
    """Update a video."""
    video = get(db_session=db_session, video_id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A video with this id does not exist."}],
        )
    return video


@router.post("", response_model=VideoRead)
def create_video(db_session: DbSession, video_in: VideoCreate):
    """Create a new video."""
    return create(db_session=db_session, video_in=video_in)


@router.put("/{video_id}", response_model=VideoRead)
def update_video(db_session: DbSession, video_id: PrimaryKey, video_in: VideoUpdate):
    """Update a video."""
    video = get(db_session=db_session, video_id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A video with this id does not exist."}],
        )
    video = update(db_session=db_session, video=video, video_in=video_in)
    return video


@router.delete("/{video_id}", response_model=None)
def delete_video(db_session: DbSession, video_id: PrimaryKey):
    """Delete a video."""
    video = get(db_session=db_session, video_id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A video with this id does not exist."}],
        )
    delete(db_session=db_session, video_id=video_id)

