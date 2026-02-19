from functions.run_python_file import run_python_file

print("--- run_python_file('calculator', 'main.py') (usage instructions) ---")
print(run_python_file("calculator", "main.py"))

print("\n--- run_python_file('calculator', 'main.py', ['3 + 5']) (calculator run) ---")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\n--- run_python_file('calculator', 'tests.py') (run calculator tests) ---")
print(run_python_file("calculator", "tests.py"))

print("\n--- run_python_file('calculator', '../main.py') (expected error) ---")
print(run_python_file("calculator", "../main.py"))

print("\n--- run_python_file('calculator', 'nonexistent.py') (expected error) ---")
print(run_python_file("calculator", "nonexistent.py"))

print("\n--- run_python_file('calculator', 'lorem.txt') (expected error) ---")
print(run_python_file("calculator", "lorem.txt"))
