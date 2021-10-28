import os
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, String, BigInteger, DateTime, BINARY, func
import sys

engine = create_engine("mysql+pymysql://root:root@127.0.0.1/pythonbd")

engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()




class UserCreation(BaseModel):
    __tablename__ = "usercreation"

    TempId = Column(Integer(), primary_key=True, nullable=False)
    username = Column(String(100), nullable=False)
    firstName = Column(String(100), nullable=True)
    lastName = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=True)
    userStatus = Column(Integer(), nullable=True)


class StudentCreation(BaseModel):
    __tablename__ = "studentcreation"

    TempId = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    avarageMark = Column(Integer(), primary_key=True)
    idOfUser = Column(String(100), nullable=True)



class User(BaseModel):
    __tablename__ = "User"

    id = Column(Integer(), primary_key=True)
    username = Column(String(100), nullable=False)
    firstName = Column(String(100), nullable=True)
    lastName = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=True)
    userStatus = Column(String(100), nullable=True)
    UserCreation_TempId = Column(Integer(), ForeignKey(UserCreation.TempId), nullable=False)


class Student(BaseModel):
    __tablename__ = "Student"

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    avarageMark = Column(Integer(), nullable=True)
    User_id = Column(Integer(), ForeignKey(User.id),nullable=False,primary_key=True)
    StudentCreation_TempId = Column(Integer(),ForeignKey(StudentCreation.TempId), nullable=False,primary_key=True)
