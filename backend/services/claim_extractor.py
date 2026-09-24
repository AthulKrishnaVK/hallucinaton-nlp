import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_claims(text: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
Extract factual claims from the given text.

Rules:
1. Extract only factual claims.
2. Break complex statements into atomic claims.
3. Each claim must be independently verifiable.
4. Do not add facts that are not present in the input.
5. Return the claims as structured JSON.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "claim_extraction",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "claims": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "integer"
                                    },
                                    "text": {
                                        "type": "string"
                                    }
                                },
                                "required": ["id", "text"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["claims"],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.choices[0].message.content)