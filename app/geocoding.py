"""
Geocoding utilities for converting addresses to latitude/longitude coordinates.
Supports Google Maps Geocoding API and Mapbox Geocoding API.
"""

import os
import httpx
from typing import Optional, Tuple

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", "")
USE_GEOCODING = os.getenv("USE_GEOCODING", "False").lower() == "true"


async def geocode_address(
    street: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    country: str = "USA"
) -> Optional[Tuple[float, float]]:
    """
    Convert an address to latitude/longitude coordinates.
    Returns (latitude, longitude) tuple or None if geocoding fails.
    """
    if not USE_GEOCODING:
        return None
    
    address_parts = []
    if street:
        address_parts.append(street)
    if city:
        address_parts.append(city)
    if state:
        address_parts.append(state)
    if zip_code:
        address_parts.append(zip_code)
    if country:
        address_parts.append(country)
    
    if not address_parts:
        return None
    
    address = ", ".join(address_parts)
    
    if GOOGLE_MAPS_API_KEY:
        coords = await geocode_with_google(address)
        if coords:
            return coords
    
    if MAPBOX_API_KEY:
        coords = await geocode_with_mapbox(address)
        if coords:
            return coords
    
    return None


async def geocode_with_google(address: str) -> Optional[Tuple[float, float]]:
    """Geocode using Google Maps Geocoding API."""
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": GOOGLE_MAPS_API_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                location = data["results"][0]["geometry"]["location"]
                return (location["lat"], location["lng"])
    except Exception as e:
        print(f"Google geocoding error: {e}")
    
    return None


async def geocode_with_mapbox(address: str) -> Optional[Tuple[float, float]]:
    """Geocode using Mapbox Geocoding API."""
    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
        params = {
            "access_token": MAPBOX_API_KEY,
            "limit": 1
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("features"):
                coordinates = data["features"][0]["geometry"]["coordinates"]
                return (coordinates[1], coordinates[0])
    except Exception as e:
        print(f"Mapbox geocoding error: {e}")
    
    return None


async def geocode_zip_code(zip_code: str, country: str = "USA") -> Optional[Tuple[float, float]]:
    """
    Geocode a ZIP code to get approximate center coordinates.
    """
    return await geocode_address(zip_code=zip_code, country=country)


async def geocode_city(city: str, state: Optional[str] = None, country: str = "USA") -> Optional[Tuple[float, float]]:
    """
    Geocode a city to get center coordinates.
    """
    return await geocode_address(city=city, state=state, country=country)
