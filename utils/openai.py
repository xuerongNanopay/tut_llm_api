import os
import io

import requests
import zipfile
from pathlib import Path

API_HOST = "https://api.openai.com/v1/"
API_HOST_SKILL = f"{API_HOST}/skills"

def _default_header():
    API_KEY = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    return headers

def create_skill(skill_folder: Path) -> str:
    """Helper function to create skill in OPEN AI.
    """

    zip_buffer = _zip_folder_to_memory(skill_folder)
    folder_name = os.path.basename(os.path.normpath(skill_folder))

    response = requests.post(
        API_HOST_SKILL,
        headers=_default_header(),
        files={
            "files": (f"{folder_name}.zip", zip_buffer, "application/zip")
        }
    )

    response.raise_for_status()

    data = response.json()

    return data['id']

def _zip_folder_to_memory(skill_folder: Path) -> io.BytesIO:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(skill_folder):
            for file in files:
                full_path = Path(root) / file
                # 👇 include top-level folder
                arcname = full_path.relative_to(skill_folder.parent)
                zipf.write(full_path, arcname)

    buffer.seek(0)
    return buffer

def delete_skill(skill_id: str) -> str:
    """Helper function to delete a skill in OPEN AI"""
    response = requests.delete(
        f"{API_HOST_SKILL}/{skill_id}",
        headers=_default_header()
    )
    
    response.raise_for_status()
    data = response.json()
    return data['object']

def retrieve_skills(skill_id: str, skill_name: str):
    """Helper function to retrieve"""

def retrieve_skill_content(skill_id: str) -> str:
    """Helper functino to retrieve skill content"""