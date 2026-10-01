# PeekAboo: Find Me Something

**A little local guide that finds places that actually match what you're looking for.**

Tell PeekAboo what you're looking for, share your location, and it searches for a few nearby places that fit. Each result comes with a Google Maps link.

Instead of giving you 40 nearby pins to sort through, PeekAboo checks whether the results actually match your request and retries the search when they don't.

```text
You:       I want vegetarian food that isn't a salad bar

PeekAboo:  ✓ Search for vegetarian restaurants nearby
           ✓ Check the results
           ✓ Pick a few relevant options

           Here are 3 spots near you:
           The Coffee Hag · 2.5 km · vegan and vegetarian kitchen
           [Open in Google Maps]
```

## Demo

https://github.com/user-attachments/assets/49fd895b-d983-4650-a06b-ab1e09e0c347

## What it can do

* **Understands natural requests.** Ask for "somewhere for a quick lunch" or "a store that sells running shoes."
* **Checks its results.** If the results don't fit, the agent can rephrase the search and try again.
* **Shows its progress.** A live checklist shows what the agent is doing.
* **Gets you there.** Every result includes a Google Maps link, with directions available for walking, cycling, or transit.
* **Doesn't guess.** It only recommends places returned by the search and is transparent about information it can't verify.

## How it works

PeekAboo is an LLM agent running in a bounded tool-calling loop.

```text
User request + location
        ↓
   Create a plan
        ↓
   Search nearby places
        ↓
   Check the results
        ↓
   ┌───────┴───────┐
   fits            doesn't fit
    ↓                   ↓
complete          rephrase + retry
    ↓
Nearby places + Google Maps links
```

The LLM handles the language understanding, so there are no hard-coded keyword rules or category mappings.

## Tools

| Tool                                 | Role                                                     |
| ------------------------------------ | -------------------------------------------------------- |
| `find_nearby_places`                 | Searches nearby places using Foursquare free-text search |
| `get_directions_link`                | Creates Google Maps directions                           |
| `create_checklist` / `mark_complete` | Shows the agent's progress in the UI                     |

## Engineering decisions

* **Free-text search:** Foursquare lets the agent search using natural-language queries instead of relying on fixed categories.
* **Bounded agent loop:** Limited to 10 tool rounds so the agent can't run indefinitely.
* **Per-request state:** Each request has its own checklist, preventing concurrent requests from sharing state.
* **Streaming progress:** Tool results update the checklist in the UI as the agent works.
* **Guardrails:** The agent only recommends places returned by the search and doesn't invent information it can't verify.

## Stack

Python · OpenAI API · Foursquare Places API · Gradio · Google Maps

```text
app.py       agent loop + Gradio UI
tools.py     tool functions + dispatcher
context.py   system prompt
styles.py    CSS + browser JavaScript
```

## Run locally

```bash
git clone https://github.com/DilashaShakya/PeekAboo-AI.git
cd PeekAboo-AI
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=...
FOURSQUARE_API_KEY=...
```

Then:

```bash
python app.py
```

Open `http://127.0.0.1:7860`, click **Let me peek nearby**, and ask for something.

## Limitations

* Ratings, reviews, and opening hours aren't currently included.
* Search radius is fixed at 5 km.
* Location is sent to OpenAI and Foursquare for the search and isn't stored by the app.
