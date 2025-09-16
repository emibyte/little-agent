import os

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    report = [] 
    if working_directory not in os.path.abspath(os.path.join(working_directory, directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    try:
        if os.path.isdir(path):
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                report.append(f"-{filename}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
            return "\n".join(report)
    except Exception as e:
        return f"Error while listing files: {e}"
                
