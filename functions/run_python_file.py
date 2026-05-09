import os
import subprocess


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