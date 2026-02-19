import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python script relative to the working directory with optional command-line arguments; returns stdout, stderr, and exit code",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the .py file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        resolved_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        in_working_dir = os.path.commonpath([working_dir_abs, resolved_path]) == working_dir_abs
        if not in_working_dir:
            raise ValueError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(resolved_path):
            raise ValueError(f'Error: "{file_path}" does not exist or is not a regular file')
        
        if not resolved_path.endswith(".py"):
            raise ValueError(f'Error: "{file_path}" is not a Python file')

        command = ["python", resolved_path]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        parts = []
        if completed_process.returncode != 0:
            parts.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            parts.append("No output produced")
        if completed_process.stdout:
            parts.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            parts.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(parts)
    except (OSError, ValueError) as e:
        return f"Error: {e}"
