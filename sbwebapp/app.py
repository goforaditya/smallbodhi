from fasthtml.common import *
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_URL= "http://" + os.getenv("API_URL") + ":" + os.getenv("API_PORT") + "/process"

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink, picolink))

messages = []

# Chat message component (renders a chat bubble)
def ChatMessage(msg):
    bubble_class = f"chat-bubble-{'primary' if msg['role'] == 'user' else 'secondary'}"
    chat_class = f"chat-{'end' if msg['role'] == 'user' else 'start'}"
    return Div(Div(msg['content'], cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}")

# The input field for the user message. Also used to clear the 
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(type="text", name='msg', id='msg-input', 
                 placeholder="Type a message", 
                 cls="input input-bordered w-full", hx_swap_oob='true')

def ContextInput():
    return Input(type="text", name='ctx', id='ctx-input', 
                 placeholder="Provide context e.g. Video url", 
                 cls="input input-bordered w-full", hx_swap_oob='true')

def send_request(message, context):
    # API endpoint URL
    url = API_URL

    # JSON payload
    payload = {
        "query": message,
        "context": context
    }

    # Send POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print("API Response:", json.dumps(result, indent=2))
        return result['llm_response']
    else:
        print("Error:", response.status_code, response.text)



# The main screen
@app.route("/")
def get():
    page = Body(H1('Chatbot Demo'),
                Div(*[ChatMessage(msg) for msg in messages],
                    id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(ChatInput(), ContextInput(), Button("Send", cls="btn btn-primary")),
                    hx_post="/", hx_target="#chatlist", hx_swap="beforeend",
                    cls="flex space-x-2 mt-2",
                ), cls="p-4 max-w-lg mx-auto")
    return Title('Chatbot Demo'), page

# Handle the form submission
@app.post("/")
def post(msg:str, ctx:str):
    
    r = send_request(msg,ctx) # get response from chat model
    messages.append({"role": "user", "content": msg})
    messages.append({"role": "assistant", "content": r})
    return (ChatMessage(messages[-2]), # The user's message
            ChatMessage(messages[-1]), # The chatbot's response
            ChatInput(),
            ContextInput()) # And clear the input field via an OOB swap


if __name__ == '__main__': uvicorn.run("basic:app", host='0.0.0.0', port=8000, reload=True)