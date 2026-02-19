import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        print(f"Result for {directory} directory:")
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise ValueError(f'"{directory}" is not a directory')

        files_info = []
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(path)
            file_size = os.path.getsize(path)
            files_info.append(f"  - {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    except (OSError, ValueError) as e:
        err = f"    Error: {e}"
        return err