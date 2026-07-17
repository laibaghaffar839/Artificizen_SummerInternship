from main import ask

buggy_code = """
def divide(a,b):
    return a/b

print(divide(10,0))
"""

default_review = ask(f"review this code:{buggy_code}")
print(f"Default_Review:\n{default_review}")
print("="*60)

reviewer_system = """
You are a senior Python code reviewer.

Rules:
- Be strict and concise.
- Do not give praise.
- Only provide actionable improvements.
- Focus on bugs, security, performance, and best practices.
"""

review = ask(f"Review this code:{buggy_code}",system=reviewer_system)
print(f"Review with System Prompt:\n{review}")

