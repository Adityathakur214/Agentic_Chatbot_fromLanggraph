import re
from datetime import datetime
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests
from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate basic arithmetic expressions using numbers, parentheses, and + - * / % **."""
    expression = expression.strip().replace('^', '**')
    if not expression or len(expression) > 100:
        return 'Error: expression is empty or too long.'
    if not re.fullmatch(r'[0-9\s+\-*/%().]+', expression):
        return 'Error: only basic arithmetic characters are allowed.'
    try:
        result = eval(expression, {'__builtins__': {}}, {})
    except ZeroDivisionError:
        return 'Error: division by zero is not allowed.'
    except Exception as exc:
        return f'Error: could not calculate expression ({exc}).'
    return str(result)


@tool
def get_current_time(timezone: str = 'Asia/Kolkata') -> str:
    """Return the current date and time for a valid IANA time-zone such as Asia/Kolkata."""
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception as exc:
        raise ValueError(
            'Invalid timezone. Use an IANA timezone such as Asia/Kolkata or America/New_York.'
        ) from exc
    return now.strftime('%Y-%m-%d %H:%M:%S %Z')


@tool
def get_weather(city: str) -> str:
    """Return current weather for a city using the public Open-Meteo geocoding and weather APIs."""
    city = city.strip()
    if not city:
        raise ValueError('City name is required.')

    geocode_url = (
        'https://geocoding-api.open-meteo.com/v1/search'
        f'?name={quote(city)}&count=1&language=en&format=json'
    )
    geocode_response = requests.get(geocode_url, timeout=10)
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()

    results = geocode_data.get('results') or []
    if not results:
        return f'No location was found for {city}.'

    location = results[0]
    latitude = location['latitude']
    longitude = location['longitude']
    resolved_name = location.get('name', city)
    country = location.get('country', '')

    weather_url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={latitude}&longitude={longitude}'
        '&current=temperature_2m,relative_humidity_2m,wind_speed_10m'
        '&timezone=auto'
    )
    weather_response = requests.get(weather_url, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    current = weather_data['current']
    units = weather_data.get('current_units', {})

    return (
        f'Current weather in {resolved_name}, {country}: '
        f"temperature {current.get('temperature_2m')} {units.get('temperature_2m', '°C')}, "
        f"humidity {current.get('relative_humidity_2m')} {units.get('relative_humidity_2m', '%')}, "
        f"wind speed {current.get('wind_speed_10m')} {units.get('wind_speed_10m', 'km/h')}."
    )


TOOLS = [calculator, get_current_time, get_weather]