from openai import OpenAI
from context import SYSTEM_PROMPT
from tools import tools, handle_tool_calls, new_checklist, get_checklist_markdown
from dotenv import load_dotenv
from styles import (
    THEME, CSS, LOCATION_JS, PAGE_HEAD,
    TITLE_HTML, CHAT_HEAD_HTML, CHAT_PLACEHOLDER,
    status_html,
)
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

# Most of the time the agent needs 4-6 rounds of tools. This stops a confused
# agent from looping forever (and spending money on every round).
MAX_STEPS = 10

openai = OpenAI()


def progress_panel(checklist, done=False):
    """A collapsible box in the chat that shows the agent's checklist."""
    return gr.ChatMessage(
        role="assistant",
        content=get_checklist_markdown(checklist) or "Getting started...",
        metadata={
            "title": "Done" if done else "Working on it...",
            "status": "done" if done else "pending",
        },
    )


def chat_message(message, history, location):
    system_prompt = SYSTEM_PROMPT

    # Add location information to the agent's context
    if location:
        lat, lon = location.split(",")

        system_prompt += (
            f"\n\n# User location\n"
            f"The user has shared their location: "
            f"latitude {lat}, longitude {lon}."
        )
    else:
        system_prompt += (
            "\n\n# User location\n"
            "The user has not shared their location. "
            "If they ask for nearby places, ask them to "
            "share their location or provide a city."
        )

    # Convert Gradio history into OpenAI messages
    history = [
        {
            "role": h["role"],
            "content": h["content"]
        }
        for h in history
        if not (h.get("metadata") or {}).get("title")
    ]

    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )

    # Each message gets its own empty checklist (not shared with other users)
    checklist = new_checklist()
    yield [progress_panel(checklist)]

    # Initial model call
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )

    # Agent loop (stops after MAX_STEPS rounds of tools)
    steps = 0
    while response.choices[0].finish_reason == "tool_calls" and steps < MAX_STEPS:
        steps += 1

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls

        # Add the assistant's tool request to the conversation
        messages.append(assistant_message)

        # Run the requested tools
        results = handle_tool_calls(tool_calls, checklist)

        # Give the tool results back to the model
        messages.extend(results)

        # Show the updated checklist in the chat while the agent keeps working
        yield [progress_panel(checklist)]

        # Let the model decide what to do next
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )

    # Hit the limit while the model still wanted tools?
    # Ask it to answer with what it has found so far, with no more tool calls.
    if response.choices[0].finish_reason == "tool_calls":
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="none"
        )

    answer = response.choices[0].message.content

    # No checklist (e.g. "hi")? Just show the answer.
    if get_checklist_markdown(checklist):
        yield [progress_panel(checklist, done=True), gr.ChatMessage(role="assistant", content=answer)]
    else:
        yield answer


# -------------------------
# Gradio UI
# -------------------------

if __name__ == "__main__":

    # fill_height=True lets the chat stretch to fill the whole browser window
    with gr.Blocks(title="Find Me Something", fill_height=True) as demo:

        # Header: location status | mascot + title (centre) | location button
        with gr.Row(elem_id="topbar"):
            location_status = gr.HTML(status_html(False), elem_id="status_box")
            gr.HTML(TITLE_HTML, elem_id="title_box")
            location_button = gr.Button(
                "Let me peek nearby",
                elem_id="peek_btn",
                scale=0
            )

        # Hidden textbox that stores "latitude,longitude"
        location_box = gr.Textbox(
            elem_id="user_location",
            visible=False
        )

        # Browser asks for location permission
        location_button.click(
            None,
            outputs=location_box,
            js=LOCATION_JS
        )

        # Update status after location is received
        location_box.change(
            lambda loc: status_html(bool(loc)),
            inputs=location_box,
            outputs=location_status
        )

        # Chat card: takes up all the remaining space
        with gr.Column(elem_id="chat_card", scale=1):
            gr.HTML(CHAT_HEAD_HTML)

            gr.ChatInterface(
                fn=chat_message,
                chatbot=gr.Chatbot(
                    elem_id="chatbot",
                    show_label=False,
                    scale=1,
                    placeholder=CHAT_PLACEHOLDER
                ),
                textbox=gr.Textbox(
                    elem_id="chat_input",
                    placeholder="I'm looking for...",
                    show_label=False,
                    container=False,
                    submit_btn=True,
                    stop_btn=True
                ),
                # None = "don't change the location box" when a chip is clicked
                examples=[
                    ["A cozy coffee shop", None],
                    ["Something fun to do", None],
                    ["Vegetarian food nearby", None]
                ],
                additional_inputs=[location_box],
                fill_height=True
            )

    demo.launch(theme=THEME, css=CSS, head=PAGE_HEAD)
