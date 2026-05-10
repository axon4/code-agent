import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        is_valid_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not is_valid_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ['python', target_file]
        
        if args:
            command.extend(args)

        sub_process = subprocess.run(command, cwd=absolute_path, capture_output=True, text=True, timeout=30)
        output = ''

        if sub_process.returncode != 0:
            output += f'Process exited with code {sub_process.returncode}\n'

        if not sub_process.stdout and not sub_process.stderr:
            output += f'No output produced'
        else:
            output += f'STDOUT:\n{sub_process.stdout}'
            output += f'STDERR:\n{sub_process.stderr}'

        return output
    except Exception as e:
        return f'Error: executing Python file: {e}'
    

schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='executes and runs a Python file at the specified path with optional arguments and returns the output. If the prompt contains instructions to run a Python file, use this function to execute the file and provide the output back to the user. If the command contains the word "run", you should probably use this function instead of `get_files_info`',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='path to the target Python file to run'
            ),
            'args': types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description='optional list of string arguments to pass to the Python file'
            )
        }
    )
)