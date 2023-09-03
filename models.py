import os
import datetime

from sqlalchemy import Column, DateTime, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Session


POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)


class Model(DeclarativeBase):
    ...


class PazamCount(Model):
    __tablename__ = 'pazam_count'

    user_id = Column(String, primary_key=True)
    day_of_release = Column(DateTime)
    rank = Column(String(10))

Model.metadata.create_all(engine)


def set_user_release_date(user_id: int, day_of_release: datetime.datetime):
    session = Session(engine)
    session.query(PazamCount).filter(PazamCount.user_id == str(user_id)).delete()

    pazam = PazamCount(
        user_id=str(user_id),
        day_of_release=day_of_release,
        rank="שצ"
    )
    session.add(pazam)
    session.commit()
    session.close()


def get_user_release_date(user_id: int) -> datetime.datetime:
    session = Session(engine)
    pazam = session.query(PazamCount).filter(PazamCount.user_id == str(user_id)).first()
    session.close()
    return pazam.day_of_release
