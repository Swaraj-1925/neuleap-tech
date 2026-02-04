from datetime import date
import httpx

async def fecth_weather_data(latitude: float, longitude: float, start_date: date, end_date: date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "temperature_2m",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(url, params=params)
        res.raise_for_status()
        return res.json()
