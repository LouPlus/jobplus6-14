from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class User(Base, UserMixin):

    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    realname =  db.Column(db.String(32))
    phone = db.Column(db.String(16))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    resume_url = db.Column(db.String(64))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'))
    company = db.relationship('Company', backref=db.backref('users', lazy='dynamic'))


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self._password, pwd)


class Company(Base):

    __tablename__ = 'company'

    name =db.Column(db.String(128), unique=True, index=True, nullable=False)
    logo = db.Column(db.String(256), nullable=False)
    site = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(100))
    about = db.Column(db.String(1000))
    tags = db.Column(db.String(128))
    stack = db.Column(db.String(128))
    field = db.Column(db.String(128))
    finance = db.Column(db.String(128))



class Job(Base):

    __tablename__ = 'job'

    name = db.Column(db.String(24))
    salary_low = db.Column(db.Integer)
    salary_high = db.Column(db.Integer)
    location = db.Column(db.String(24))
    description = db.Column(db.String(1000))
    experience = db.Column(db.String(32))
    degree = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)
    is_open = db.Column(db.Boolean, default=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', backref=db.backref('jobs', lazy='dynamic'))



class Application(Base):

    __tablename__ = 'application'

    WAITING = 1
    REJECT = 2
    ACCEPT = 3

    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=WAITING)
    response = db.Column(db.String(256))
