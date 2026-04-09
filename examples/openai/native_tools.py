from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI
from pydantic import BaseModel

default_gpt_model="gpt-5.4-mini"
client = OpenAI()

def tool_weather():
    answer = client.responses.create(
        model=default_gpt_model,
        input="Who is the current president of France?",
        tools=[{"type": "web_search_preview"}]
    )
    print(answer.output)

if __name__ == "__main__":
    tool_weather()