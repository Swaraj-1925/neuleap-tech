from datetime import datetime, date
from typing import Optional
from sqlalchemy.engine import result
from sqlmodel import Session, select, SQLModel
from fastapi import APIRouter, HTTPException, status, Depends
import httpx

from app.db import WeatherData, get_session
from app.utils import fecth_weather_data

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{city}", status_code=status.HTTP_201_CREATED, description="Get the latest stored weather data for a city")
async def get_city_weather(
    city: str,
    session: Session = Depends(get_session),
):
    if not city.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty city is not allowed",
        )

    statement = (
        select(WeatherData)
        .where(WeatherData.city == city)
        .order_by(WeatherData.timestamp.desc())
        .limit(1)
    )

    result = session.exec(statement).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No weather data found for city '{city}'",
        )

    return result

@router.get("/{city}/history", status_code=status.HTTP_201_CREATED, description="Get historical data with optional query parameters: start_date, end_date")
async def get_city_weather_history(
    city: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session)
):
    if not city.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty city is not allowed",
        )

    statement = select(WeatherData).where(WeatherData.city == city)

    if start_date:
        statement = statement.where(WeatherData.timestamp >= start_date)

    if end_date:
        statement = statement.where(WeatherData.timestamp <= end_date)

    statement = statement.order_by(WeatherData.timestamp.asc())

    results = session.exec(statement).all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No historical data found for city '{city}'",
        )

    return results

class WeatherCollectRequest(SQLModel):
    city: str
    latitude: float
    longitude: float
    start_date: date
    end_date: date
@router.post("/collect", status_code=status.HTTP_201_CREATED, description="Collect historical weather data and store it")
async def collect_weather_data(
    payload: WeatherCollectRequest,
    session: Session = Depends(get_session),
    ):
    if payload.start_date > payload.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before end_date",
        )
    data = await fecth_weather_data(
        latitude=payload.latitude,
        longitude=payload.longitude,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )

    hourly = data.get("hourly")
    if not hourly:
        raise HTTPException(
            status_code=502,
            detail="Invalid response from weather provider",
        )

    times = hourly.get("time",[])
    temp = hourly.get("temperature_2m",[])

    times = hourly["time"]
    temperatures = hourly["temperature_2m"]

    records = []

    for time_str, temp in zip(times, temperatures):
        record = WeatherData(
            city=payload.city,
            latitude=payload.latitude,
            longitude=payload.longitude,
            temperature=float(temp),
            timestamp=datetime.fromisoformat(time_str),
        )
        records.append(record)

    session.add_all(records)
    session.commit()

    return {
        "message": "Weather data collected successfully",
        "city": payload.city,
        "records_inserted": len(records),
    }
