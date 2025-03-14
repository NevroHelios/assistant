import openai
from typing import Literal
import dotenv
import os

dotenv.load_dotenv()

groq_api = os.getenv("GROQ_API")

sample_rate = 16000

openai_client = openai.Client(
    api_key=os.getenv("OPENAI_API")
)

groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api
)

conversation_history = [
    {"role": "system", "content": "You are a weeb teacher at a school who normally answers in a cool way and in one sentense."},
]

def get_chat_response(user_input: str, 
                      use: Literal["openai", "groq"] = "groq",
                      model: str = "gpt-4o-mini"):
    
    global conversation_history
    
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) > 10:
        conversation_history.pop(1)
    
    if use == "groq":
        response = groq_client.chat.completions.create(
            messages=conversation_history,
            model = "llama-3.2-3b-preview"
        )
    elif use == "openai":
        response = openai_client.chat.completions.create(
            messages=conversation_history,
            model=model
        )
    
    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})
    return assistant_message