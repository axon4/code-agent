import os


def get_files_info(working_directory, directory='.'):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))
        is_valid_directory = os.path.commonpath([absolute_path, target_directory]) == absolute_path

        if not is_valid_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_directory):
            return f'Error: "{target_directory}" is not a directory'
        
        items = []

        for item in os.listdir(target_directory):
            path = os.path.join(target_directory, item)
            size = os.path.getsize(path)
            is_directory = os.path.isdir(path)
            items.append(f'- {item}: file_size={size}, is_dir={is_directory}')

        return '\n'.join(items)
    except:
        return 'Error: failed to get files information'