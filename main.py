from dotenv import load_dotenv
import os
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from tools import available_functions, call_function


def main():
    argument_parser = argparse.ArgumentParser(description='Code Agent')
    argument_parser.add_argument('prompt', type=str, help='<prompt>')
    argument_parser.add_argument('--verbose', action='store_true', help='enable verbose output')
    arguments = argument_parser.parse_args()

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    model = os.environ.get('GEMINI_MODEL', 'gemini-3.1-flash-lite')

    if not api_key:
        raise RuntimeError('error finding Gemini API Key')

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role='user', parts=[types.Part(text=arguments.prompt)])]
    temperature = None
    response = client.models.generate_content(
        # model='gemini-2.5-flash',
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            tools=[available_functions]
        )
    )

    if response.usage_metadata is None:
        raise RuntimeError('error contacting Gemini API')

    if arguments.verbose:
        print(f'User prompt: {arguments.prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)

            if not function_call_result.parts:
                raise Exception('error: no parts returned from function-call--result parts')
            
            response = function_call_result.parts[0].function_response

            if response is None:
                raise Exception('error: no 1st-level function-response')
            
            function_response = response.response

            if function_response is None:
                raise Exception('error: no 2nd-level function-response')
            
            function_results = []
            function_results.append(function_call_result.parts[0])

            if arguments.verbose:
                print(f'-> {function_call_result.parts[0].function_response.response}')

    else:
        print(f'Response:')
        print(response.text)


if __name__ == '__main__':
    main()