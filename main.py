import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from functions.prompts import system_prompt


def chat_completion_create(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    return response


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("The OpenRouter API Key is not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = chat_completion_create(client, messages)
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Response:\n{message.content}")
            sys.exit(0)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                # function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

        if response.usage is None:
            raise RuntimeError("Usage metadata is not found")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

    print("Error: Model reached maximum iteration limit without completing.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
