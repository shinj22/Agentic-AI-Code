from config import MAX_CHARS
from functions.get_file_content import get_file_content

content = get_file_content("calculator", "lorem.txt")

# lorem.txt is > 20,000 chars, so it should be truncated at MAX_CHARS
assert len(content) == MAX_CHARS + len(
    f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
), f"Expected length MAX_CHARS + truncation message, got {len(content)}"

truncation_msg = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
assert content.endswith(truncation_msg), f"Content should end with truncation message, got ending: ...{content[-80:]!r}"

print("get_file_content('calculator', 'lorem.txt') truncates correctly: length =", len(content), ", ends with truncation message.")

print("\n--- get_file_content('calculator', 'main.py') ---")
print(get_file_content("calculator", "main.py"))

print("\n--- get_file_content('calculator', 'pkg/calculator.py') ---")
print(get_file_content("calculator", "pkg/calculator.py"))

print("\n--- get_file_content('calculator', '/bin/cat') (expected error) ---")
print(get_file_content("calculator", "/bin/cat"))

print("\n--- get_file_content('calculator', 'pkg/does_not_exist.py') (expected error) ---")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
