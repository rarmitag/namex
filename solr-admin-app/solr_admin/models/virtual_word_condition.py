
from . import db
from sqlalchemy.schema import Column


class VirtualWordCondition(db.Model):

    cnd_id = Column(db.Integer, primary_key=True)
    word_id = Column(db.Integer, primary_key=True)

    rc_consenting_body = Column(db.VARCHAR(195))
    rc_words = Column(db.VARCHAR(1000))
