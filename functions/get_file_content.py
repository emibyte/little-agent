from functions.config import LIMIT_TO_TRUNCATE_FILE
import os

def get_file_content(working_directory, file_path):
    file_contents = ""
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_path_working_dir = os.path.abspath(working_directory)

    try:
        if not abs_path.startswith(abs_path_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Unknown error checking file status and directory: {e}"

    try:
        with open(abs_path, "r") as f:
            file_contents = f.read(LIMIT_TO_TRUNCATE_FILE)
        return file_contents
    except Exception as e:
        return f"Unknown error reading file: {e}"
