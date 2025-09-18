import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes content to a file within the working directory. Creates the file if it does not exist.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to write to the file.",
            ),
        },
        required = ["file_path", "content"],
    )
)

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    abs_path_file = os.path.abspath(path)
    abs_path_working_dir = os.path.abspath(working_directory)

    if not abs_path_file.startswith(abs_path_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(abs_path_file)):
        try:
            os.makedirs(os.path.dirname(abs_path_file))
        except Exception as e:
            return f'Error: Could not create directory "{path}"'

    if os.path.exists(abs_path_file) and os.path.isdir(abs_path_file):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(abs_path_file, "w") as f:
            bytes_written = f.write(content)
            return f'Successfully wrote to "{file_path}" ({bytes_written} characters written)'
    except IOError as e:
        return f'Error: Could not write to file "{file_path}": {e}'
