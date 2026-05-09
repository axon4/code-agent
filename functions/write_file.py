import os


def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        is_valid_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not is_valid_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(absolute_path, exist_ok=True)

        with open(target_file, 'w') as file:
            file.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return 'Error: failed to write file'