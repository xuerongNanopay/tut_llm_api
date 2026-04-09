# CLI for Open AI API.

import os
import io
import sys
from pathlib import Path
import zipfile
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

API_HOST = "https://api.openai.com/v1/"
API_HOST_SKILL = f"{API_HOST}/skills"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def list_skills():
    response = requests.get(
        API_HOST_SKILL,
        headers=headers
    )

    print(response.json())

def retrieve_skill(skill_id: str):
    response = requests.get(
        f"{API_HOST_SKILL}/{skill_id}",
        headers=headers
    )

    print(response.content)

def retrieve_skill_content(skill_id: str):
    response = requests.get(
        f"{API_HOST_SKILL}/{skill_id}/content",
        headers=headers
    )

    print_zip_contents(response.content)

def delete_skill(skill_id: str):
    response = requests.delete(
        f"{API_HOST_SKILL}/{skill_id}",
        headers=headers
    )

    print(response.content)


def create_agent_skill(relative_path: str):
    path = Path(relative_path).expanduser().resolve()
    zip_buffer = zip_folder_to_memory(path)
    folder_name = os.path.basename(os.path.normpath(path))

    response = requests.post(
        API_HOST_SKILL,
        headers=headers,
        files={
            "files": (f"{folder_name}.zip", zip_buffer, "application/zip")
        }
    )
    print(response.content)

def zip_folder_to_memory(folder_path: Path) -> io.BytesIO:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = Path(root) / file
                # 👇 include top-level folder
                arcname = full_path.relative_to(folder_path.parent)
                zipf.write(full_path, arcname)

    buffer.seek(0)
    return buffer

def print_zip_contents(zip_bytes: bytes):
    buffer = io.BytesIO(zip_bytes)

    with zipfile.ZipFile(buffer, "r") as zipf:
        for name in zipf.namelist():
            print(f"\n>>>>>> {name}")

            # skip directories
            if name.endswith("/"):
                continue

            with zipf.open(name) as f:
                try:
                    content = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    content = "<binary content>"
                
                print(content)

            print(f"\n====== {name}")


if __name__ == "__main__":
    list_skills()

    # retrieve_skill("skill_69d8160e358081909df65d25015f00d8001c67d04a78726c")
    # retrieve_skill_content("skill_69d8160e358081909df65d25015f00d8001c67d04a78726c")
    # delete_skill("skill_69d8160e358081909df65d25015f00d8001c67d04a78726c")
    # input_path = sys.argv[1]
    # create_agent_skill(input_path)
