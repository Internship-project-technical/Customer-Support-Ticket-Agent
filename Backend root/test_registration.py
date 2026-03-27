import requests

print("=" * 60)
print("Testing Registration")
print("=" * 60)

response = requests.post(
    'http://localhost:8000/auth/register',
    json={
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '1234567890',
        'password': 'test123'
    }
)

print('Status:', response.status_code)

if response.status_code == 200:
    user = response.json()
    print('✓ Registration successful!')
    print(f'  User ID: {user.get("user_id")}')
    print(f'  Name: {user.get("name")}')
    print(f'  Email: {user.get("email")}')
else:
    print('✗ Failed:', response.text)
