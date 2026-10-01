

# PeekAboo: Find Me Something

**Your little local guide that finds the *right* places, not just nearby ones.** Tell Peekaboo what you're in the mood for, share your location with one click, and it comes back with a few spots that actually match, each one a tap away in Google Maps.

Search "food near me" in most apps and you get 40 pins to sort through yourself. Peekaboo is built to get it right for you: it reads what you actually asked for, checks every result against your request, throws out anything that doesn't fit, and searches again if the first try misses. Ask for coffee and you get coffee shops, not the smoke shop next door.

```
You:       I want vegetarian food that isn't a salad bar

Peekaboo:  ✓ Search for vegetarian restaurants nearby
           ✓ Check they're actually restaurants
           ✓ Pick the closest good options

           Here are 3 spots near you:
           The Coffee Hag · 2.5 km · vegan and vegetarian kitchen   [Open in Google Maps]
           ...
```

## Demo



https://github.com/user-attachments/assets/49fd895b-d983-4650-a06b-ab1e09e0c347



## What it can do

- **Understands what you mean.** "Somewhere to grab a quick lunch", "a pharmacy", "a store that sells running shoes": no fixed menu of categories.
- **Double-checks its own work.** If the search brings back a smoke shop when you asked for coffee, Peekaboo notices, drops it, and searches again.
- **Shows its plan while it works.** A live checklist ticks off each step, so you're never staring at a spinner.
- **One tap to get there.** Every place comes with a Google Maps link. Want to walk or bike instead? Just ask.
- **Honest.** It only recommends places it actually found, and it tells you what it couldn't check, like opening hours.

## How it works

Peekaboo is an LLM agent running in a loop. The model decides which tool to call, looks at what comes back, and keeps going until it has a good answer.

```
"Where can I buy running shoes?" + your location
        ↓
  Make a plan ─────────────────────► create_checklist     (streams live to the chat)
        ↓
  Search ──────────────────────────► find_nearby_places   (Foursquare free-text search)
        ↓
  Do these results fit? Shoe stores? Close by?
        ↓                 └── no ──► rephrase ("sports store"), search again
  Tick off steps ──────────────────► mark_complete
        ↓
  3 nearby stores with Google Maps links
```

The LLM does all the language understanding. There are no keyword rules or category mappings: the model's own wording goes straight into the search, which is why it can handle requests nobody planned for.

## Tools

| Tool | Role |
|---|---|
| **`find_nearby_places`** | **Core tool.** Free-text place search around the user's coordinates. Returns name, categories, distance and a Maps link per result, trimmed so the model can judge relevance cheaply. |
| `get_directions_link` | Google Maps directions for walking, cycling or transit. |
| `create_checklist` / `mark_complete` | The agent's plan, streamed to the UI so users see progress while it works. |

## Engineering decisions

- **API chosen for the agent, not popularity.** Geoapify and OSM search by category, which forces a hand-written mapping and can't express requests like "running shoes". Foursquare accepts free-text queries, so the LLM can rephrase and retry on its own.
- **Bounded agent loop.** Capped at 10 tool rounds. If it hits the cap, a final call with `tool_choice="none"` makes the model answer with what it has, instead of failing.
- **Failures go back to the model.** API errors and timeouts are returned as tool results, so the agent can explain or retry instead of crashing.
- **Per-request state.** Each request gets its own checklist, so concurrent users never share state.
- **Streaming progress.** The chat handler is a generator: each tool round `yield`s an updated plan to the UI.
- **Prompt guardrails.** The agent only recommends places returned by the search, and it says so when it can't verify something (hours, ratings, "vibe").

## Stack

Python · OpenAI API (`gpt-5.4-mini`) · Foursquare Places API · Gradio · Google Maps URLs

```
app.py       agent loop + Gradio UI
tools.py     tool functions, JSON schemas, tool dispatcher
context.py   system prompt
styles.py    theme, CSS, browser JS (geolocation, animations)
```

## Run locally

```bash
git clone https://github.com/DilashaShakya/PeekAboo-AI.git
cd PeekAboo-AI
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=...
FOURSQUARE_API_KEY=...    # Service API Key from foursquare.com/developers
```

```bash
python app.py
```

Open http://127.0.0.1:7860, click **Let me peek nearby**, and ask for something.

## Limitations and next steps

- No ratings, reviews or opening hours (paid Foursquare fields). The agent picks the closest relevant matches and says what it couldn't check.
- Fixed 5 km radius. Next step: let the agent widen it when results are sparse.
- Location is sent to OpenAI and Foursquare to run the search and isn't stored by the app.
