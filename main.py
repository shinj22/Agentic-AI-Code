import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import AGENT_LOOP_LIMIT
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if (args.verbose):
        print("User prompt: " + args.user_prompt)

    for _ in range(AGENT_LOOP_LIMIT):
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        functionResults = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                    raise RuntimeError(f"Empty function response for {function_call.name}")
                result = function_call_result.parts[0].function_response.response
                if args.verbose:
                    print(f"-> {result}")
                functionResults.append(function_call_result.parts[0])
        else:
            print("Final Response: " + response.text)
            break
        
        messages.append(types.Content(role="user", parts=functionResults))
    
if __name__ == "__main__":
    main()