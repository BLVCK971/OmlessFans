from datetime import datetime
from typing import List, Optional
from collections import defaultdict


from pydantic import validator, Field

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType
from pydantic.networks import EmailStr, AnyHttpUrl

from omless.database.core import Base
from omless.models import Pagination, ResourceMixin, ResourceBase, NameStr, PrimaryKey

from omless.modules.don.models import DonRead
from omless.modules.omless.models import OmlessRead

class Video(Base ,ResourceMixin):
    id = Column(Integer, primary_key=True)
    created_at: Optional[datetime] = Field(None, nullable=True)
    weblink: Optional[AnyHttpUrl] = Field(None, nullable=True)
	


# Pydantic models...
class VideoBase(ResourceBase):
    description: Optional[str] = Field(None, nullable=True)
    name: NameStr
    created_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(None, nullable=True)

class VideoCreate(VideoBase):
    omless: OmlessRead
    dons: Optional[List[DonRead]] = []

class VideoRead(VideoBase):
    id: PrimaryKey
    omless: Optional[OmlessRead]

class VideoPagination(Pagination):
    items: List[VideoRead] = []