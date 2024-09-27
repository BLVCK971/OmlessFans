from typing import List, Optional
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from datetime import datetime

from omless.enums import VideoResourceReferenceTypes
from omless.exceptions import ExistsError

from .models import Video, VideoCreate, VideoUpdate


def get(*, db_session, video_id: int) -> Optional[Video]:
    """Returns a video based on the given video id."""
    return db_session.query(Video).filter(Video.id == video_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Video]]:
    """Returns all videos."""
    return db_session.query(Video)


def create(*, db_session, video_in: VideoCreate) -> Video:
    """Create a new video."""
    video = Video(**video_in.dict())
    db_session.add(video)
    db_session.commit()
    return video


def get_or_create(*, db_session, video_in) -> Video:
    """Gets a video by it's resource_id or creates a new video."""
    if hasattr(video_in, "resource_id"):
        q = db_session.query(Video).filter(Video.resource_id == video_in.resource_id)
    else:
        q = db_session.query(Video).filter_by(**video_in.dict())

    instance = q.first()
    if instance:
        return instance

    return create(db_session=db_session, video_in=video_in)


def update(*, db_session, video: Video, video_in: VideoUpdate) -> Video:
    """Updates a video."""
    video_data = video.dict()
    update_data = video_in.dict(skip_defaults=True)

    for field in video_data:
        if field in update_data:
            setattr(video, field, update_data[field])

    db_session.commit()
    return video


def delete(*, db_session, video_id: int):
    """Deletes a video."""
    db_session.query(Video).filter(Video.id == video_id).delete()
    db_session.commit()