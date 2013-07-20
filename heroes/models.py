from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from Flasktest.database import Base
from heroes.views import db


class Heroes(db.Model):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)
    hometown = Column(String(30), unique=False)
    branch_of_service = Column(String(30), unique=False)
    rank = Column(String(30), unique=False)
    story = Column(Text(350), unique=False)
    photo = Column(Text(100), unique=False)
    email = Column(String(30), unique=True)

class Supporters(db.Model):
    __tablename__ = 'supporters'
    id = Column(Integer, primary_key=True)
    fb_email = Column(String(30), unique=False)
    fbuid = Column(Integer, primary_key=True)
    fb_name = Column(String(30), unique=False)
    profile_pic = Column(Text(100), unique=False)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    supporter_id = Column(Integer, ForeignKey('supporters.id'))
    text_message = Column(Text(120), unique=False)
    instagram_url = Column(Text(200), unique=False)
