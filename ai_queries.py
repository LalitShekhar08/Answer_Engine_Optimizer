import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from google import genai

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("OPENAI KEY LOADED:", bool(OPENAI_API_KEY))
print("ANTHROPIC KEY LOADED:", bool(ANTHROPIC_API_KEY))
print("GEMINI KEY LOADED:", bool(GEMINI_API_KEY))

# Clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def query_gpt(query):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Recommend top brands/products for: {query}
                    
                    Return:
                    - Brand names
                    - Why they are recommended
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"GPT Error: {str(e)}"


def query_claude(query):
    try:
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Recommend top brands/products for: {query}
                    
                    Return:
                    - Brand names
                    - Why they are recommended
                    """
                }
            ]
        )

        return response.content[0].text

    except Exception as e:
        return f"Claude Error: {str(e)}"


def query_gemini(query):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            Recommend top brands/products for: {query}

            Return:
            - Brand names
            - Why they are recommended
            """
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"


def query_all_ais(query):
    results = {
        "GPT-4": query_gpt(query),
        "Claude": query_claude(query),
        "Gemini": query_gemini(query)
    }

    print("\n========== AI RESPONSES ==========")

    for ai, response in results.items():
        print(f"\n{ai}:")
        print(response[:500])

    return results