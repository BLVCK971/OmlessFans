from typing import Optional
from datetime import datetime, timedelta

from pydantic.fields import Field
from pydantic.networks import EmailStr, AnyHttpUrl
from pydantic import BaseModel
from pydantic.types import conint, constr, SecretStr

from sqlalchemy import Boolean, Column, DateTime, Integer, String, event, ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
OrganizationSlug = constr(regex=r"^[\w]+(?:_[\w]+)*$", min_length=3)

# SQLAlchemy models...
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


class ResourceMixin(TimeStampMixin):
    """Resource mixin."""

    resource_type = Column(String)
    resource_id = Column(String)
    weblink = Column(String)



# Pydantic models...
class OmlessFanBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%d-%m-%Y_T%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }

class Pagination(OmlessFanBase):
    itemsPerPage: int
    page: int
    total: int

class PrimaryKeyModel(BaseModel):
    id: PrimaryKey


class ResourceBase(OmlessFanBase):
    resource_type: Optional[str] = Field(None, nullable=True)
    resource_id: Optional[str] = Field(None, nullable=True)
    weblink: Optional[AnyHttpUrl] = Field(None, nullable=True)