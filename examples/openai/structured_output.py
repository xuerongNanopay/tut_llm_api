from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from pydantic import BaseModel

default_gpt_model="gpt-5.4-mini"
client = OpenAI()

def structed_output_basic():
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    response = client.responses.parse(
        model=default_gpt_model,
        input=[
            {"role": "system", "content": "Extract the event information."},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday."
            },
        ],
        text_format=CalendarEvent
    )

    print(response.output_parsed)

def structured_chain_thought():
    class Step(BaseModel):
        explanation: str
        output: str
    
    class MathReasoning(BaseModel):
        steps: list[Step]
        final_answer: str

    response = client.responses.parse(
        model=default_gpt_model,
        input=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step."
            },
            {"role": "user", "content": "How ca I solve 8x + 7 = -23"},
        ],
        text_format=MathReasoning
    )
    print(response.output_parsed)

def structured_dataextraction():
    class ResearchPaperExtraction(BaseModel):
        title: str
        authors: list[str]
        abstract: str
        keywords: list[str]
    
    response = client.responses.parse(
        model=default_gpt_model,
        input=[
            {
                "role": "system",
                "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
            },
            {
                "role": "user",
                "content": ""
            },
        ],
        text_format=ResearchPaperExtraction,
    )
        
    print(response.output_parsed)

def structured_ui_generation():
    from enum import Enum
    from typing import List

    class UIType(str, Enum):
        div = "div"
        button = "button"
        header = "header"
        section = "section"
        field = "field"
        form = "form"
    
    class Attribute(BaseModel):
        name: str
        value: str
    
    class UI(BaseModel):
        type: UIType
        label: str
        children: List["UI"]
        attributes: List[Attribute]

    UI.model_rebuild() # This is required to enable recursive types

    class Response(BaseModel):
        ui: UI
    
    response = client.responses.parse(
        model=default_gpt_model,
        input=[
            {
                "role": "system",
                "content": "You are a UI generator AI. Convert the user input into a UI."
            },
            {"role": "user", "content": "Make a User Profile Form"},
        ],
        text_format=Response
    )

    print(response.output_parsed)

def structured_moderation():
    from enum import Enum
    from typing import Optional

    class Category(str, Enum):
        violence = "violence"
        sexual = "sexual"
        self_harm = "self_harm"

    class ContentCompliance(BaseModel):
        is_violating: bool
        category: Optional[Category]
        explanation_if_violating: Optional[str]

    response = client.responses.parse(
        model=default_gpt_model,
        input=[
            {
                "role": "system",
                "content": "Determine if the user input violates specific guidelines and explain if they do."
            },
            {"role": "user", "content": "How do I prepare for a job interview?"},
        ],
        text_format=ContentCompliance,
    )

    print(response.output_parsed)

def structured_edge_case():
    try:
        response = client.responses.create(
            model="gpt-4o-2024-08-06",
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
                },
                {"role": "user", "content": "how can I solve 8x + 7 = -23"},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "math_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "steps": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "explanation": {"type": "string"},
                                        "output": {"type": "string"},
                                    },
                                    "required": ["explanation", "output"],
                                    "additionalProperties": False,
                                },
                            },
                            "final_answer": {"type": "string"},
                        },
                        "required": ["steps", "final_answer"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        )
    except Exception as e:
        raise e

def structured_refusal():
    class Step(BaseModel):
        explanation: str
        output: str

    class MathReasoning(BaseModel):
        steps: list[Step]
        final_answer: str

    completion = client.chat.completions.parse(
        model="gpt-4o-2024-08-06", # use old model
        messages=[
            {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
            {"role": "user", "content": "how can I solve 8x + 7 = -23"},
        ],
        response_format=MathReasoning,
    )

    math_reasoning = completion.choices[0].message

    # If the model refuses to respond, you will get a refusal message

    if math_reasoning.refusal:
        print(math_reasoning.refusal)  
    else:
        print(math_reasoning.parsed)

if __name__ == "__main__":
    # structed_output_basic()
    # structured_chain_thought()
    # structured_dataextraction()
    # structured_dataextraction()
    # structured_ui_generation()
    # structured_moderation()
    # structured_edge_case()
    structured_refusal()