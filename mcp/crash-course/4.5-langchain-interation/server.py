import requests 
import asyncio
import json
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
        response = requests.get(
            f"{weather_api_url}{latitude},{longitude}",

            headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/geo+json"
        }
        )

        if response.status_code == 200:
            data = dict(response.json())
            state = data.get("properties", {}).get("gridId", "Unknown")
            gridx = data.get("properties", {}).get("gridX", "Unknown")
            gridy = data.get("properties", {}).get("gridY", "Unknown")
            ret = {
                "state": state,
                "gridx": gridx,
                "gridy": gridy
            }

            print(f"Retrieved state: {state}, gridX: {gridx}, gridY: {gridy}")

            return json.dumps(ret)  # <-- FIXED: return as string
        else:
            return json.dumps({"error": "Unable to retrieve weather data."})
    except Exception as e:
        return json.dumps({"error": str(e)})


# NW_latitude = "47.6062"
# NW_longitude = "-122.3321"

# result = asyncio.run(get_state_and_qrid(NW_longitude, NW_latitude))
# print(result)

if __name__ == "__main__":
    runtype = "sse2"  # Change to "sse" for SSE transport

    if runtype == "sse":
        server.run ("sse")
    else:
        server.run(transport="stdio")

