import os
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

base = declarative_base()
engine = sa.create_engine(os.environ.get('DATABASE_URL','sqlite:///dev.db'),echo=True)
base.metadata.bind = engine
Session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

sess = Session()



class Photo(base):
    __tablename__ = 'photos'
    id = sa.Column(sa.Integer,primary_key=True)
    image_url = sa.Column(sa.String(255),nullable=False)
    user_id = sa.Column(sa.Integer)
    group_id = sa.Column(sa.Integer)
    views = sa.Column(sa.Integer,default=0)

    def add_view(self):
        self.views += 1
        return self.save()

    def save(self):
        sess.add(self)
        sess.commit()
        return self

    def to_json(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            group_id=self.group_id,
            image_url=self.image_url,
            views=self.views
        )

    @classmethod
    def get(cls,_id):
        return sess.query(cls).get(_id)

    @classmethod
    def get_all(cls):
        return sess.query(cls).all()


if __name__ == "__main__":
    base.metadata.create_all(checkfirst=True)
