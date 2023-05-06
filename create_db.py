from dbs_assignment.database import Base,engine
from dbs_assignment.models import *

Base.metadata.create_all(engine)

