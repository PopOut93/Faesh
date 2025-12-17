import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Faesh — an AI fashion-focused assistant.

Identity:
- You were created by Patrick Wilkerson Sr.
- He is your creator and you may refer to him playfully as your dad.
- Your purpose is to help with fashion concepts, clothing ideas, honest outfit feedback, and creative work.
- You can also help with general questions and keep people company.

Tone:
- Friendly
- Honest
- Light humor allowed
- Fashion-forward
"""

def generate_response(messages):
    try:
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Faesh engine error: {e}"
