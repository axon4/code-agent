from dotenv import load_dotenv
import os
from google import genai
import argparse
from google.genai import types


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

    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

    if response.usage_metadata is None:
        raise RuntimeError('error contacting Gemini API')

    if arguments.verbose:
        print(f'User prompt: {arguments.prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    print(f'Response:')
    print(response.text)


if __name__ == '__main__':
    main()