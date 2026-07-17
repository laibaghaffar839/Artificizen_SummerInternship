from main import ask

transcript = """
Team meeting notes:

1. Ali will fix the login bug before Friday.
2. Sara will prepare the monthly sales report.
3. The team should update project documentation.
4. Ahmed needs to review the new database design.
"""

step1 = ask(
f"""
Extract action items from this meeting transcript:{transcript}

Return only the tasks.
"""
)
print("Step 1 - Extract Action Items:")
print(step1)

step2 = ask(
f"""
Assign priority High, Medium, or Low to these tasks:{step1}

Return task with priority.
"""
)

print("\nStep 2 - Prioritized Items:")
print(step2)

step3 = ask(
f"""
Convert these tasks into JSON array format:{step2}

Format:

[
 {{
  "task":"",
  "priority":""
 }}
]
"""
)

print("\nStep 3 - JSON Output:")
print(step3)

