import requests
import bcrypt

print("=" * 60)
print("Fix User Password (Hash)")
print("=" * 60)

# This will update the user's password to a proper bcrypt hash
# But we need to do this through the API or directly via MySQL

# Option 1: Use the registration endpoint (it hashes automatically)
print("\nOption 1: Re-register with proper hash")
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
    print("✓ Re-registration successful! Password is now hashed.")
    print(f"  User: {response.json()}")
elif response.status_code == 400 and "already registered" in response.text:
    print("User already exists. We need to update password directly.")
    print("\nOption 2: Update password via MySQL Workbench")
    
    # Generate a hash manually
    password = "test123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    print(f"\nGenerated hash for 'test123':")
    print(f"  {hashed.decode('utf-8')}")
    
    print("\nPlease run this SQL in MySQL Workbench:")
    print("-" * 60)
    print(f"UPDATE users SET hashed_password = '{hashed.decode('utf-8')}' WHERE email = 'test@example.com';")
    print("-" * 60)
else:
    print(f"Error: {response.text}")
