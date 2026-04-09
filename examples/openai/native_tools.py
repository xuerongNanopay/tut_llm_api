from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI
from pydantic import BaseModel

default_gpt_model="gpt-5.4-mini"
client = OpenAI()

def tool_web_search_preview():
    answer = client.responses.create(
        model=default_gpt_model,
        input="Who is the current president of France?",
        tools=[{"type": "web_search_preview"}]
    )
    print(answer.output)

def tool_web_search():
    response = client.responses.create(
        model="gpt-5",
        tools=[{"type": "web_search"}],
        input="What was a positive news story from today?"
    )

    print(response.output)

if __name__ == "__main__":
    # tool_web_search_preview()
    tool_web_search()