import os
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)

# Foursquare's place search API
PLACES_URL = "https://places-api.foursquare.com/places/search"

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


# Give the tools to OpenAI
tools = [
    {
        "type": "function",
        "function": find_nearby_places_json,
    },
    {
        "type": "function",
    },
]


# Connect the tool names to our Python functions
tool_map = {
    "find_nearby_places": find_nearby_places,
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
