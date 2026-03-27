import requests

print("=" * 60)
print("Registering a new user")
print("=" * 60)

register_data = {
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "password": "test123"
}

response = requests.post(
    'http://localhost:8000/auth/register',
    json=register_data
)

if response.status_code == 200:
    print("✓ Registration successful!")
    print(f"  User created: {response.json()}")
else:
    print(f"✗ Registration failed: {response.text}")
    print(f"Status code: {response.status_code}")
