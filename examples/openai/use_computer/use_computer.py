# 
# This script is expensive to run.
# 

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import base64

client = OpenAI()
advance_gpt_model="gpt-5.4"

response = client.responses.create(
    model=advance_gpt_model,
    tools=[{"type": "computer"}],
    input="Check whether the Filters panel is open. If it is not open, click Show filters. Then type penguin in the search box. Use the computer tool for UI interaction.",
)

print(response.output)

def send_computer_screenshot(response, call_id, screenshot_base64):
    return client.responses.create(
        model="gpt-5.4",
        tools=[{"type": "computer"}],
        previous_response_id=response.id,
        input=[
            {
                "type": "computer_call_output",
                "call_id": call_id,
                "output": {
                    "type": "computer_screenshot",
                    "image_url": f"data:image/png;base64,{screenshot_base64}",
                    "detail": "original",
                },
            }
        ],
    )

def computer_use_loop(target, response):
    from local_browser import capture_screenshot, handle_computer_actions

    while True:
        computer_call = next(
            (item for item in response.output if item.type == "computer_call"),
            None,
        )
        if computer_call is None:
            return response
        
        handle_computer_actions(target, computer_call.actions)

        screenshot = capture_screenshot(target)
        screenshot_base64 = base64.b64decode(screenshot).decode("utf-8")

        response = client.responses.create(
            model=advance_gpt_model,
            tools=[{"type": "computer"}],
            previous_response_id=response.id,
            input=[
                {
                    "type": "computer_call_output",
                    "call_id": computer_call.call_id,
                    "output": {
                        "type": "computer_screenshot",
                        "image_url": f"data:image/png;base64,{screenshot_base64}",
                        "detail": "original",
                    },
                }
            ]
        )
        
def _run():
    response = client.responses.create(
        model=advance_gpt_model,
        tools=[{"type": "computer"}],
        input="Check whether the Filters panel is open. If it is not open, click Show filters. Then type penguin in the search box. Use the computer tool for UI interaction.",
    )

    print(response.output)
    # TODO: The function is expensive. complete when nee.


if __name__ == "__main__":
    pass