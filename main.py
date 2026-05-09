from dotenv import load_dotenv
import os
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError('error finding Gemini API Key')

    client = genai.Client(api_key=api_key)

    prompt = 'lorem ipsum dolor sit amet, consectetur adipiscing elit'
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)

    if response.usage_metadata == None:
        raise RuntimeError('error contacting Gemini API')

    print(f'prompt: {prompt}')
    print(f'prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'response tokens: {response.usage_metadata.candidates_token_count}')
    print(f'response:')
    print(response.text)


if __name__ == '__main__':
    main()