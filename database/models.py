from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=False, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    registration_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    advertisements: Mapped[List["Advertisement"]] = relationship(
        back_populates="owner", cascade="all, delete"
    )

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }


class Advertisement(Base):
    __tablename__ = "app_advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("app_user.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="advertisements")

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "heading": self.heading,
            "owner_id": self.owner_id,
        }
