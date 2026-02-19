import os

from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file relative to the working directory, truncated to a maximum character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        resolved_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, resolved_path]) == working_dir_abs
        if not valid_target_dir:
            raise ValueError(f'Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(resolved_path):
            raise ValueError(f'File not found or is not a regular file: "{file_path}"')

        with open(resolved_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except (OSError, ValueError) as e:
        return f"Error: {e}"