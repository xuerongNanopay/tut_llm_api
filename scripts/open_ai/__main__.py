# CLI for Open AI API.

import requests
import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

API_HOST = "https://api.openai.com/v1/"
API_HOST_SKILL = urljoin(API_HOST, "skills")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def list_skills():
    response = requests.get(
        API_HOST_SKILL,
        headers=headers
    )

    print(response.json())


if __name__ == "__main__":
    list_skills()