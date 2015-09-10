import os
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

base = declarative_base()
engine = sa.create_engine(os.environ.get('DATABASE_URL','sqlite:///dev.db'),echo=True)
base.metadata.bind = engine



class Photo(base):
    __tablename__ = 'photos'
    id = sa.Column(sa.Integer,primary_key=True)
    image_url = sa.Column(sa.String(255),nullable=False)
    user_id = sa.Column(sa.Integer)
    group_id = sa.Column(sa.Integer)
    views = sa.Column(sa.Integer,default=0)


if __name__ == "__main__":
    base.metadata.create_all()
