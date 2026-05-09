from dotenv import load_dotenv
import os
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError('error finding API Key')

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model='gemini-2.5-flash', contents='lorem ipsum dolor sit amet, consectetur adipiscing elit')

    print(response.text)


if __name__ == '__main__':
    main()