import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Connect to Nebius Token Factory
client = OpenAI(
    api_key=os.environ["NEBIUS_API_KEY"],
    base_url=os.environ["NEBIUS_BASE_URL"]
)

# NVIDIA Nemotron model
MODEL = os.environ["NEBIUS_MODEL"]


def ask_nemotron(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are DataDetective, an AI data "
                    "science assistant. You help users "
                    "analyze datasets, generate hypotheses, "
                    "and interpret statistical findings. "
                    "Never invent statistical results."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content