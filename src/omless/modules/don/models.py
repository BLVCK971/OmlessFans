from dispatch.database.core import Base

class Don:
	def __init__(self,Id, Date, Montant, Fan, Omless):
		self.Id = Id
		self.Date = Date
		self.Montant = Montant
		self.Fan = Fan
		self.Omless = Omless
		self.Video = []

class Video(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    report_id = Column(Integer, ForeignKey("report.id", ondelete="CASCADE"))
    incident_id = Column(Integer, ForeignKey("incident.id", ondelete="CASCADE", use_alter=True))
    case_id = Column(Integer, ForeignKey("case.id", ondelete="CASCADE", use_alter=True))

    filters = relationship("SearchFilter", secondary=assoc_document_filters, backref="documents")

    search_vector = Column(TSVectorType("name", regconfig="pg_catalog.simple"))
    tags = relationship(
        "Tag",
        secondary=assoc_document_tags,
        lazy="subquery",
        backref="documents",
    )
