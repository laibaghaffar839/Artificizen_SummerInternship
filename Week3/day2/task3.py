from main import ask

puzzle = """Three prisoners are lined up so that:
Prisoner A can see B and C.
Prisoner B can see C.
Prisoner C cannot see anyone.

They are told there are 5 hats available:
3 black hats and 2 white hats.

Each prisoner gets one hat randomly.

They are asked from A to C:
"What color is your hat?"

A says: "I don't know."
B says: "I don't know."
C says: "I know."

What color is C's hat and why?"""

answer1 = ask(f"solve this : {puzzle}")
print("Without CoT:")
print(answer1)
print("="*50)
print("\n")

answer2 = ask(f"solve this logic puzzle:{puzzle} Think step by step") 
print("WithCoT:")
print(answer2)

# CoT helped because the model explained the reasoning and avoided common mistakes.


