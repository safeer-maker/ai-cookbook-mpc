import os 
import json
import requests 


from mcp.server.fastmcp import FastMCP

server = FastMCP(
    name="weather",
    host="0.0.0.0",
    port=4567
)


@server.tool()
async def get_weather(longitude: str, latitude: str) -> str:
    """Retrieve the weather for a given location.

    Args:
        longitude (str): The longitude of the location.
        latitude (str): The latitude of the location.
    """
    
    weather_api_url = "https://api.weather.gov/points/"

    try:
        response = await requests.get(
            f"{weather_api_url}{latitude},{longitude}"
        )

        if response.status_code == 200:
            data = dict (response.json())
            return (data)
        else:
            return {"error": "Unable to retrieve weather data."}
    except Exception as e:
        return {"error": str(e)}


NW_latitude = "47.6062"
NW_longitude = "-122.3321"

result =  get_weather(NW_longitude, NW_latitude)
