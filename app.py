from openai import OpenAI
from context import SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from dotenv import load_dotenv
from styles import CSS, LOCATION_JS
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

openai = OpenAI()


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
    ]

    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )

    # Initial model call
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )

    # Agent loop
    while response.choices[0].finish_reason == "tool_calls":

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls

        # Add the assistant's tool request to the conversation
        messages.append(assistant_message)

        # Run the requested tools
        results = handle_tool_calls(tool_calls)

        # Give the tool results back to the model
        messages.extend(results)

        # Let the model decide what to do next
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )

    return response.choices[0].message.content


# -------------------------
# Gradio UI
# -------------------------

if __name__ == "__main__":

    with gr.Blocks() as demo:

        gr.Markdown("# Find Me Something 🔎")

        # Hidden textbox that stores "latitude,longitude"
        location_box = gr.Textbox(
            elem_id="user_location",
            visible=False
        )

        # Location button
        location_button = gr.Button(
            "📍 Share my location",
            size="sm"
        )

        location_status = gr.Markdown(
            "Location not shared yet."
        )

        # Browser asks for location permission
        location_button.click(
            None,
            outputs=location_box,
            js=LOCATION_JS
        )

        # Update status after location is received
        location_box.change(
            lambda loc: (
                "✅ Location shared."
                if loc
                else "Location not shared yet."
            ),
            inputs=location_box,
            outputs=location_status
        )

        # Chat interface
        gr.ChatInterface(
            fn=chat_message,
            title="Find Me Something",
            chatbot=gr.Chatbot(show_label=False),
            additional_inputs=[location_box]
        )

    demo.launch(css=CSS)