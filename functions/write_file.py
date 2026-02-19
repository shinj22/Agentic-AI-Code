import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path relative to the working directory; creates parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        resolved_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, resolved_path]) == working_dir_abs
        if not valid_target_dir:
            raise ValueError(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        if not os.path.isdir(os.path.dirname(resolved_path)):
            raise ValueError(f'Cannot write to "{file_path}" as the directory does not exist')
        
        os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
        with open(resolved_path, "w") as f:
            f.write(content)
        return f"File {file_path} written successfully ({len(content)} characters written)"
    except (OSError, ValueError) as e:
        return f"Error: {e}"