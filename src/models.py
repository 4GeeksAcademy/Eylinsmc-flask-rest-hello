from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(15), unique=False, nullable=True)
    lastname: Mapped[str] = mapped_column(String(15), unique=False, nullable=True)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    caption: Mapped[str] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum("image", "video", name="media_type"), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="media")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_from = relationship("User", foreign_keys=[user_from_id], backref="following")
    user_to = relationship("User", foreign_keys=[user_to_id], backref="followers")