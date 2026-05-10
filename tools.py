from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
import os
from configuration import WORKING_DIRECTORY


available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)


def call_function(function_call, verbose=False):
    if verbose:
        print(f'calling function: {function_call.name}({function_call.args})')
    else:
        print(f' - calling function: {function_call.name}')

    functions = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file
    }

    function_name = function_call.name or ''

    if function_name not in functions:
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={'error': f'unknown function: {function_name}'}
                )
            ]
        )
    else:
        arguments = dict(function_call.args) if function_call.args else {}
        arguments['working_directory'] = os.environ.get('WORKING_DIRECTORY') or WORKING_DIRECTORY
        function_result = functions[function_name](**arguments)

        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={'result': function_result}
                )
            ]
        )