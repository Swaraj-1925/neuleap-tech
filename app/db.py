from typing import Optional
import os
from datetime import datetime

from sqlmodel import (
        Field,
        SQLModel,
        create_engine,
        TIMESTAMP,
        Column,
        text,
        Session
        )


class WeatherData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(index=True)

    latitude: float
    longitude: float
    temperature: float

    timestamp: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    try:
        # SQLModel.metadata.drop_all(engine)
        # print("Drop all tables")
        SQLModel.metadata.create_all(engine)
        print("DB created successfully")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        raise

def get_session():
    with Session(engine) as session:
        yield session


