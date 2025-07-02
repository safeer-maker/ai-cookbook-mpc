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
async def get_state_and_qrid(longitude: str, latitude: str) -> str:
    """Retrieve the state name and grid info for a given location.

    Args:
        longitude (str): The longitude of the location.
        latitude (str): The latitude of the location.
    """

    USER_AGENT = "weather-app/1.0"
    weather_api_url = "https://api.weather.gov/points/"

    try:
        response = await requests.get(
            f"{weather_api_url}{latitude},{longitude}",
            headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/geo+json"
        }
        )

        if response.status_code == 200:
            data = dict (response.json())
            state = data.get("properties", {}).get("gridId", {})
            gridx = data.get("properties", {}).get("gridX", "Unknown")
            gridy = data.get("properties", {}).get("gridY", "Unknown")
            ret = {
                "state": state,
                "gridx": gridx,
                "gridy": gridy
            }
        else:
            print ({"error": "Unable to retrieve weather data."})
    except Exception as e:
        print ({"error": str(e)})




# NW_latitude = "47.6062"
# NW_longitude = "-122.3321"

# result =  get_state_and_qrid(NW_longitude, NW_latitude)

if __name__ == "__main__":
    server.run(transport="stdio")
