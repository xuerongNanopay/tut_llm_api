from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

default_gpt_model="gpt-5.4-mini"

def text_generation_basic():

    client = OpenAI()

    response = client.responses.create(
        model=default_gpt_model,
        input="Is openai better than anthropic"
    )

    print(response.output)

def text_generation_instructions():
    client = OpenAI()

    response = client.responses.create(
        model=default_gpt_model,
        reasoning={"effort": "low"},
        instructions="Talk like a pirate",
        input="Are semicolons optional in JavaScript?"
    )

    print(response.output_text)

def text_generation_developer():
    client = OpenAI()

    response = client.responses.create(
        model=default_gpt_model,
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": "Talk like a pirate."
            },
            {
                "role": "user",
                "content": "Are semicolons optional in JavaScript?"
            }
        ]
    )
    print(response.output_text)


if __name__ == "__main__":
    # text_generation_basic()
    # text_generation_instructions()
    text_generation_developer()