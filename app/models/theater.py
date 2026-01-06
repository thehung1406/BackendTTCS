from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Theater(SQLModel, table=True):
    __tablename__ = "theaters"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    address: str = Field(max_length=255)
    city: str = Field(max_length=50)

    image: Optional[str] = Field(default=None, max_length=255)
    rating: Optional[float] = None

    technologies: Optional[Dict] = Field(
        default=None,
        sa_column=Column(JSONB)
    )
    special: Optional[str] = Field(default=None, max_length=50)
