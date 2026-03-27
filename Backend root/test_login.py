import requests

print("=" * 60)
print("Testing Login")
print("=" * 60)

# Login
response = requests.post(
    'http://localhost:8000/auth/login',
    data={'username': 'test@example.com', 'password': 'test123'}
)

if response.status_code == 200:
    token_data = response.json()
    print("✓ Login successful!")
    print(f"  Token: {token_data['access_token'][:50]}...")
    
    # Get user info
    print("\n" + "=" * 60)
    print("Getting User Info")
    print("=" * 60)
    
    headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
    user_response = requests.get('http://localhost:8000/auth/me', headers=headers)
    
    if user_response.status_code == 200:
        print("✓ User info retrieved!")
        print(f"  User: {user_response.json()}")
    else:
        print(f"✗ Failed: {user_response.text}")
else:
    print(f"✗ Login failed: {response.text}")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
