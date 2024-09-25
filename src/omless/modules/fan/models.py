from dispatch.database.core import Base

class Fan:
	def __init__(self, id, Email, Password, Nom, Prénom, Ville):
		self.id = id
		self.Email = Email
		self.Password = Password
		self.Nom = Nom
		self.Prénom = Prénom
		self.Ville = Ville

        # Fan.Omless()
        # Fan.Don()

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
