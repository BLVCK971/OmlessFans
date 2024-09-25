from dispatch.database.core import Base

class Omless:
	def __init__(self,Id, Nom, Prénom, Etat, Ville):
		self.Id = Id
		self.Nom = Nom
		self.Prénom = Prénom
		self.Etat = Etat
		self.Ville = Ville
		self.Video = []
		self.Don = []
		self.Fan = []


class Omless(Base ,ResourceMixin):
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    etat = Column(String)
    ville = Column(String)
    name = Column(String)
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