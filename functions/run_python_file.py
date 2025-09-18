import os
from subprocess import run, CalledProcessError
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Run a python file via the python interpreter installed on the system and returns the output of the interpreter",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path of the file to run via the python interpreter, relative to the working directory. Has to be a file with the file-extension .py",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type = types.Type.STRING,
                    description = "Optional arguments to pass to the Python file.",
                ),
                description = "Optional arguments to pass to the Python file.",
            ),
        },
        required = ["file_path"],
    )
)

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    abs_path_file = os.path.abspath(path)
    abs_path_working_dir = os.path.abspath(working_directory)

    if not abs_path_file.startswith(abs_path_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.exists(abs_path_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        arguments = ["python3", file_path]
        for arg in args:
            arguments.append(arg)
        process = run(args=arguments,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=abs_path_working_dir,
                    timeout=30)
        result = []
        if process.stdout:
            result.append(f"STDOUT:\n{process.stdout}")
        if process.stderr:
            result.append(f"STDERR:\n{process.stderr}")
        if process.returncode != 0:
            result.append(f"Process exited with code {process.returncode}")

        if len(result) > 0:
            return "\n".join(result)
        else:
            return "No output produced"
        
    except CalledProcessError as e:
        return f"Error: executing Python file: {e}."

