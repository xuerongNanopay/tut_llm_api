import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

from utils.openai import create_skill, delete_skill

default_gpt_model="gpt-5.4-mini"
advance_gpt_model="gpt-5.4"

client = OpenAI()


def skill_nba_final():
    # 
    fold_path = Path(__file__).resolve().parent
    path = (fold_path / "../../skills/sql-nba-finals").resolve()
    skill_id = create_skill(path)
    delete_skill(skill_id)
    # response = client.responses.create(
    #     model=default_gpt_model,
    #     input="genarate output from sql-nba-finals",
    #     tools=[
    #         {
    #             "type": "shell",
    #             "environment": {
    #                 "type": "local",
    #                 "skills": [
    #                     {
    #                         "name": "sql-nba-finals",
    #                         "description": "Retrieve stats from NBA finals, and format them into SQL insertion statement.",
    #                         "path": f"{str(path)}"
    #                     }
    #                 ]
    #             }
    #         }
    #     ]
    # )

    # print(response.output_text)

if __name__ == "__main__":
    skill_nba_final()