import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("The OpenRouter API Key is not found")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,

)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

if response.usage is None:
    raise RuntimeError("Usage metadata is not found")

# print(f"User Prompt: {}")
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Prompt tokens: {response.usage.completion_tokens}")
print(f"Response:\n{response.choices[0].message.content}")
