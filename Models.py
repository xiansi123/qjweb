# -*- coding: utf-8 -*-
from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone=db.Column(db.String(13),nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #questons=db.relationship('Question',backref=db.backref('author'),lazy='dynamic')
    role=db.Column(db.String(10), nullable=False,default='student')
    #1表示在校学生2表示研究生3表示出国4表示工作5表示老师
    state=db.Column(db.Integer,default=1)
    #1表示找导师2表示考研3表示出国4表示工作
    intention=db.Column(db.Integer)

class Follow(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower=db.Column(db.Integer,db.ForeignKey('user.id'))
    following=db.Column(db.Integer,db.ForeignKey('user.id'))

class Question(db.Model):
    __tablename__ ='questions'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(120),nullable=False)
    content=db.Column(db.Text,nullable=False)
    create_time= db.Column(db.DateTime,default=datetime.now())
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class Stu(db.Model):
    __tablename__='stu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    no = db.Column(db.String(16), nullable=False)
    school=db.Column(db.String(16))
    name = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    age = db.Column(db.String(16))
    major = db.Column(db.String(16))
    depart = db.Column(db.String(16))
    term = db.Column(db.String(16))#学期
    others = db.Column(db.Text)
#传递函数依赖
class Tea(db.Model):
    __tablename__='tea'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    no = db.Column(db.String(16))
    school = db.Column(db.String(16))
    name = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    willings=db.Column(db.Text)
    major_in = db.Column(db.Text)
    others = db.Column(db.Text)
#考研党
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school = db.Column(db.String(20))  # 研究生学校
    city = db.Column(db.String(20))
    name = db.Column(db.String(16))
    depart = db.Column(db.String(16))
    age = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    major = db.Column(db.String(20))  # 研究生专业
    grades = db.Column(db.Integer)
    others=db.Column(db.Text)
    advice=db.Column(db.Text)
#出国党
class Abroad(db.Model):
    __tablename__ = 'abroad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country = db.Column(db.String(20))#国家
    city = db.Column(db.String(20))
    name = db.Column(db.String(16))
    age = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    school = db.Column(db.String(20))  # 留学学校
    major = db.Column(db.String(20))  # 专业
    TOELF = db.Column(db.Integer)#托福
    IELTS=db.Column(db.Integer)#雅思
    advice = db.Column(db.Text)
    others = db.Column(db.Text)
#工作党
class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    city=db.Column(db.String(20))
    content=db.Column(db.String(20))
    salary=db.Column(db.Integer)
    name = db.Column(db.String(16))
    age = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    company=db.Column(db.String(20))
    advice = db.Column(db.Text)
    others = db.Column(db.Text)
