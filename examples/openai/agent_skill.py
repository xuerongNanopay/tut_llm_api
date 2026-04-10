import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

from utils.openai import create_skill, delete_skills, delete_skill, retrieve_skills, retrieve_skill

default_gpt_model="gpt-5.4-mini"
advance_gpt_model="gpt-5.4"

client = OpenAI()


def skill_nba_final():
    skill_name = "sql-nba-finals"
    delete_skills(skill_name)
    
    fold_path = Path(__file__).resolve().parent
    path = (fold_path / f"../../skills/{skill_name}").resolve()
    new_skill = create_skill(path)

    time.sleep(10) # add sleep for OPENAI to stablize the uploaded skill

    response = client.responses.create(
        model=default_gpt_model,
        input="genarate output from sql-nba-finals",
        tools=[
            {
                "type": "shell",
                "environment": {
                    "type": "container_auto",
                    "skills": [
                        {
                            "type": "skill_reference", 
                            # "skill_id": f"{skill['id']}",
                            "skill_id": new_skill['id'],
                            "version": new_skill['default_version']
                        },
                    ]
                }
            }
        ]
    )
    print(response.output_text)
    delete_skill(new_skill['id'])


if __name__ == "__main__":
    skill_nba_final()