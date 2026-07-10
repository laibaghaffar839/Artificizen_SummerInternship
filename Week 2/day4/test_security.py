from security import hash_password, verify_password

password = "hello123"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

print()

print("Correct Password:")
print(
    verify_password(
        "hello123",
        hashed
    )
)

print()

print("Wrong Password:")
print(
    verify_password(
        "abc123",
        hashed
    )
)