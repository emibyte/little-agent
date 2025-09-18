import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    print("Hello from little-agent!")
    if len(sys.argv) < 2:
        print("Please provide a prompt")
        sys.exit(1)
    verbose = len(sys.argv) >= 3 and sys.argv[2] == "--verbose"
    prompt = sys.argv[1]
    messages = [ types.Content(role="user", parts=[types.Part(text=prompt)]), ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt
                                                ),
                                              )

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        try:
            function_call_result = call_function(function_call_part, verbose)
            if verbose:
                print(f"{function_call_result.parts[0].function_response.response}")
        except Exception as e:
            print(f"Unknown error: {e}")
                
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
