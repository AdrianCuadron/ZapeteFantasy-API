from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, primary_key=True)
    hashed_password = Column(String)
    name = Column(String)
    last_name = Column(String)
    points = Column(Integer)
    money = Column(Double)

    profile_image_url = Column(String, name='profile_image', default="/app/images/placeholder.png")
    
    players = relationship("Player", back_populates="user")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=True)
    team = Column(String)
    position = Column(String)
    line_up = Column(Boolean)
    points = Column(Integer)
    price = Column(Double)
    state = Column(String)

    user = relationship("User", back_populates="players")
    
    