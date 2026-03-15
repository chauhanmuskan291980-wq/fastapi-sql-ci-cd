from .databse import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


class Post(Base):
    __tablename__ = "newposts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    published = Column(
        Boolean,
        nullable=False,
        server_default=text('true')
    )


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text('now()')
    )