from dotenv import load_dotenv
import os
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from tools import available_functions, call_function
from configuration import MAX_AGENT_LOOP_ITERATIONS
import sys


def main():
    argument_parser = argparse.ArgumentParser(description='Code Agent')
    argument_parser.add_argument('prompt', type=str, help='<prompt>')
    argument_parser.add_argument('--verbose', action='store_true', help='enable verbose output')
    arguments = argument_parser.parse_args()

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError('error finding Gemini API Key')

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role='user', parts=[types.Part(text=arguments.prompt)])]

    if arguments.verbose:
        print(f'User prompt: {arguments.prompt}')

    for _ in range(MAX_AGENT_LOOP_ITERATIONS):
        try:
            response = generate_content(client, messages, arguments.verbose)

            if response:
                print('response:')
                print(response)

                return
        except Exception as error:
            print(f'error generating content: {error}')

    print(f'maximum agent-loop iterations ({MAX_AGENT_LOOP_ITERATIONS}) reached')
    sys.exit(1)


def generate_content(client, messages, verbose):
    temperature = None
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            tools=[available_functions]
        )
    )

    if response.usage_metadata is None:
        raise RuntimeError('error contacting Gemini API')

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    if not response.candidates:
        raise RuntimeError('error: no candidates returned')

    for candidate in response.candidates:
        if candidate.content:
            messages.append(candidate.content)

    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call)

            if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                raise Exception('error: invalid function response')
            
            function_results.append(function_call_result.parts[0])

            if verbose:
                print(f'-> {function_call_result.parts[0].function_response.response}')

        messages.append(types.Content(role='user', parts=function_results))
    else:
        return response.text


if __name__ == '__main__':
    main()