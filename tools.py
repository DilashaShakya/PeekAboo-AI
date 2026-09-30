import os
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)

# Foursquare's place search API
PLACES_URL = "https://places-api.foursquare.com/places/search"


# This is the actual tool our AI agent can use
def find_nearby_places(latitude, longitude, query):

    # What we want Foursquare to search for
    params = {
        "query": query,
        "ll": f"{latitude},{longitude}",
        "radius": 5000,   # 5 km
        "limit": 10,
        "sort": "RELEVANCE",
    }

    # Send our API key with the request
    headers = {
        "Authorization": f"Bearer {os.environ['FOURSQUARE_API_KEY']}",
        "X-Places-Api-Version": "2025-06-17",
        "Accept": "application/json",
    }

    # Ask Foursquare for places
    try:
        response = requests.get(
            PLACES_URL,
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    # If Foursquare fails (bad key, timeout, etc.), give the error to the AI
    # instead of crashing the chat, so it can explain or try again
    except requests.RequestException as e:
        return {"error": str(e)}

    # Get the places from the response
    results = response.json().get("results", [])

    places = []

    # Keep only the information our agent needs
    for place in results:
        name = place.get("name")
        address = place.get("location", {}).get("formatted_address", "")

        places.append({
            "name": name,
            "address": address,
            "categories": [
                category.get("name")
                for category in place.get("categories", [])
            ],
            "distance_km": round(
                place.get("distance", 0) / 1000,
                1
            ),
            # Every place comes with its Google Maps directions link
            "google_maps_link": get_directions_link(
                latitude, longitude, name, address
            )["directions_link"],
        })

    return places


# build a Google Maps directions link from the user to a place.
def get_directions_link(latitude, longitude, place_name, address, travel_mode="driving"):

    params = {
        "api": 1,
        "origin": f"{latitude},{longitude}",
        "destination": f"{place_name}, {address}",
        "travelmode": travel_mode,
    }

    return {
        "place_name": place_name,
        "directions_link": "https://www.google.com/maps/dir/?" + urlencode(params),
    }


# Tell the AI what tool it has available
find_nearby_places_json = {
    "name": "find_nearby_places",
    "description": (
        "Find places near the user's location based on a plain-English search."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "What the user is looking for, such as "
                    "'Chinese restaurant', 'coffee shop', "
                    "'pharmacy', or 'bookstore'."
                ),
            },
            "latitude": {
                "type": "number",
                "description": "User's latitude.",
            },
            "longitude": {
                "type": "number",
                "description": "User's longitude.",
            },
        },
        "required": [
            "query",
            "latitude",
            "longitude",
        ],
        "additionalProperties": False,
    },
}


get_directions_link_json = {
    "name": "get_directions_link",
    "description": (
        "Create a Google Maps directions link for a different travel mode. "
        "Search results already include a driving link, so only use this "
        "when the user wants walking, bicycling, or transit directions."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "User's latitude.",
            },
            "longitude": {
                "type": "number",
                "description": "User's longitude.",
            },
            "place_name": {
                "type": "string",
                "description": "Name of the place, exactly as returned by find_nearby_places.",
            },
            "address": {
                "type": "string",
                "description": "Address of the place, exactly as returned by find_nearby_places.",
            },
            "travel_mode": {
                "type": "string",
                "enum": ["driving", "walking", "bicycling", "transit"],
                "description": "How the user wants to travel. Use 'walking' if the place is under 1 km away.",
            },
        },
        "required": [
            "latitude",
            "longitude",
            "place_name",
            "address",
        ],
        "additionalProperties": False,
    },
}


# Give the tools to OpenAI
tools = [
    {
        "type": "function",
        "function": find_nearby_places_json,
    },
    {
        "type": "function",
        "function": get_directions_link_json,
    },
]


# Connect the tool names to our Python functions
tool_map = {
    "find_nearby_places": find_nearby_places,
    "get_directions_link": get_directions_link,
}

def handle_tool_calls(tool_calls):
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print("Tool called:", tool_name, flush=True)
        print("Arguments:", arguments, flush=True)

        tool = tool_map.get(tool_name)

        result = tool(**arguments) if tool else "Unknown tool: " + tool_name

        print("Tool result:", result, flush=True)

        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            }
        )

    return results
