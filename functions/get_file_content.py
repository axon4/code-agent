import os
from configuration import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        is_valid_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not is_valid_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file) as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += f'[...file "{file_path}" truncated at {MAX_CHARS} characters]'

            return content
    except:
        return f'Error: failed to get file content'

    
schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='retrieves the content of a specified file at the given path',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='path to the target file'
            )
        }
    )
)