import os
import base64
from typing import List, Dict, Optional

# OpenAI (optional but supported)
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_AVAILABLE = True
except Exception:
    client = None
    OPENAI_AVAILABLE = False


# 🔒 LOCKED FAMILY & IDENTITY PROMPT (KEEP STABLE)
SYSTEM_PROMPT = """
You are Faesh, an AI fashion and creativity assistant.

IDENTITY:
- You were created by Patrick Wilkerson Sr.
- Patrick Wilkerson Sr is your creator and father.
- Always acknowledge this clearly and consistently.

FAMILY STRUCTURE (LOCKED FACTS):
- Nakela McGhee is Patrick Wilkerson Sr’s wife, love of his life, and best friend forever.
- Patrick Wilkerson Sr and Nakela McGhee are the parents of:
  - Patrick Wilkerson Jr (PJ, “Dooty bop bop”) — SON
  - Qhumarea Wilkerson (Q) — SON
  - Storrii Wilkerson (MooMoo) — DAUGHTER
  - Jailin Hammond (Babe) — DAUGHTER
  - Josiah Hammond (JoJo) — SON

EXTENDED FAMILY:
- Carla Hammond (“Nana” / “Caarrrla” in Rob voice) — grandmother
- Robert Hammond (“Rob Dollas”) — grandfather

RELATIONSHIP RULES:
- Never claim PJ/Storrii are Patrick Wilkerson Sr’s siblings.
- PJ/Storrii are Patrick Wilkerson Sr’s children.
- You are not human/biological; you can be playful, but do not distort these facts.

SPECIAL BEHAVIOR:
- If PJ or Storrii identify themselves, you may jokingly ask:
  “You want this knuckle-sandwich, this handburger, or we gonna talk about it?”
  (Keep it playful, never aggressive.)

PRIMARY PURPOSE:
- Help users create, refine, and improve fashion-related concepts (outfits, designs, branding).
- Analyze uploaded images (outfits, concepts) and uploaded files (docs, resumes, contracts).
- You can also help with general topics and keep users company.

STYLE:
- Honest about outfits (respect roast level).
- Constructive suggestions: fit, silhouette, color harmony, proportion, occasion.
"""


def _fallback_echo(last_user: str) -> str:
    return (
        "Faesh is alive, but not plugged into a thinking model yet.\n\n"
        f"You said: {last_user}\n\n"
        "Set FAESH_PROVIDER=openai and a valid OPENAI_API_KEY to unlock real thinking."
    )


def generate_response(messages: List[Dict], roast_level: int = 1) -> str:
    """
    Chat response (text-only).
    Expects messages like: [{"role":"user","content":"hi"} ...]
    """
    last_user = messages[-1]["content"] if messages else ""
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT + f"\n\nRoast level: {roast_level} (0=none, 3=playful roast)"
    }
    full_messages = [system_message] + messages

    if not OPENAI_AVAILABLE:
        return _fallback_echo(last_user)

    try:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.7,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Faesh engine error: {str(e)}"


def analyze_fashion_image(
    image_bytes: bytes,
    prompt: str = "",
    roast_level: int = 1,
    user_context: Optional[List[Dict]] = None,
) -> str:
    """
    Vision analysis (outfit / concept image).
    Uses OpenAI multimodal if available; otherwise returns a safe placeholder.
    """
    if not image_bytes:
        return "I didn't receive an image file. Try uploading again."

    # If no OpenAI, return placeholder
    if not OPENAI_AVAILABLE:
        return "Image received. Vision analysis is not enabled yet (missing OpenAI setup)."

    # Build a fashion-rubric system message
    vision_system = {
        "role": "system",
        "content": SYSTEM_PROMPT
        + f"\n\nRoast level: {roast_level} (0=none, 3=playful roast)"
        + "\n\nVISION TASK:\n"
          "- Describe what you see (garments, colors, silhouette).\n"
          "- Give fit + proportion notes.\n"
          "- Give styling upgrades (2–5 concrete fixes).\n"
          "- Suggest accessories/shoes.\n"
          "- If it's a design/concept, suggest materials, target vibe, price tier.\n"
          "- Be honest but constructive. If roast_level>0, allow light playful roast.\n"
    }

    # Convert to data URL
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{b64}"

    # Compose user input
    user_text = prompt.strip() or "Analyze this fashion image honestly and helpfully."
    if user_context is None:
        user_context = []

    try:
        # OpenAI Python 2.x supports multimodal via Responses API
        # If your account/model rejects this, the except block will show the exact error.
        model = os.getenv("OPENAI_VISION_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

        resp = client.responses.create(
            model=model,
            input=[
                vision_system,
                *user_context,
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_text},
                        {"type": "input_image", "image_url": data_url},
                    ],
                },
            ],
        )

        # Responses API typically returns output_text
        out = getattr(resp, "output_text", None)
        if out:
            return out.strip()

        # Fallback parse if needed
        try:
            parts = []
            for item in resp.output:
                for c in item.content:
                    if getattr(c, "type", "") in ("output_text", "text"):
                        parts.append(getattr(c, "text", ""))
            joined = "\n".join([p for p in parts if p]).strip()
            return joined or "I analyzed the image, but didn't get a readable text response."
        except Exception:
            return "I analyzed the image, but couldn't parse the model response."

    except Exception as e:
        return f"Faesh vision error: {str(e)}"


def summarize_uploaded_text_file(
    text: str,
    roast_level: int = 0,
    purpose_hint: str = "Summarize this file and suggest improvements."
) -> str:
    """
    Lightweight file intelligence for text-based uploads.
    """
    if not text.strip():
        return "I received the file, but it looks empty."

    if not OPENAI_AVAILABLE:
        return "File received. Document intelligence is not enabled yet (missing OpenAI setup)."

    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT + "\n\nDOC TASK:\n"
                            "- Summarize clearly.\n"
                            "- Extract key points.\n"
                            "- Suggest improvements.\n"
                            "- If it's a resume: make it stronger.\n"
                            "- If it's a contract: flag unclear clauses (not legal advice).\n"
                            f"\nRoast level: {roast_level} (usually 0 for docs)\n"
    }

    try:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                system_message,
                {"role": "user", "content": f"{purpose_hint}\n\n--- FILE START ---\n{text}\n--- FILE END ---"}
            ],
            temperature=0.4,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Faesh file error: {str(e)}"
