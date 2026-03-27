import requests

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Complete API Test Suite")
print("=" * 60)

# 1. Register
print("\n1. Registering user...")
register_data = {
    'name': 'Harshith',
    'email': 'harshith@example.com',
    'phone': '9876543210',
    'password': 'harshith123'
}
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)

if response.status_code == 200:
    user = response.json()
    print("✓ Registration successful!")
    print(f"   User ID: {user.get('user_id')}")
    print(f"   Name: {user.get('name')}")
    print(f"   Email: {user.get('email')}")
else:
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

# 2. Login
print("\n2. Logging in...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={'username': 'harshith@example.com', 'password': 'harshith123'}
)

if response.status_code != 200:
    print("✗ Login failed:", response.text)
    exit()

token_data = response.json()
token = token_data["access_token"]
print("✓ Login successful!")
print(f"   Token: {token[:50]}...")

# 3. Get current user
print("\n3. Getting current user...")
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

if response.status_code == 200:
    print("✓ User info retrieved!")
    print(f"   Name: {response.json().get('name')}")
    print(f"   Email: {response.json().get('email')}")
else:
    print("✗ Failed:", response.text)

# 4. Create a ticket
print("\n4. Creating a ticket...")
ticket_data = {
    'title': 'My First Support Ticket',
    'description': 'I need help with the login system',
    'email': 'harshith@example.com',
    'name': 'Harshith'
}
response = requests.post(f"{BASE_URL}/tickets/", json=ticket_data, headers=headers)

if response.status_code == 200:
    ticket = response.json()
    print("✓ Ticket created successfully!")
    print(f"   Ticket ID: {ticket.get('ticket_id')}")
    print(f"   Title: {ticket.get('title')}")
    print(f"   Status: {ticket.get('status')}")
else:
    print("✗ Failed:", response.text)

# 5. Create multiple tickets
print("\n5. Creating multiple tickets...")
tickets_list = [
    {
        'title': 'Billing Issue',
        'description': 'My credit card was charged twice',
        'email': 'harshith@example.com',
        'name': 'Harshith'
    },
    {
        'title': 'Technical Support',
        'description': 'Unable to access my account',
        'email': 'harshith@example.com',
        'name': 'Harshith'
    },
    {
        'title': 'Feature Request',
        'description': 'Add dark mode to the application',
        'email': 'harshith@example.com',
        'name': 'Harshith'
    }
]

for ticket in tickets_list:
    response = requests.post(f"{BASE_URL}/tickets/", json=ticket, headers=headers)
    if response.status_code == 200:
        t = response.json()
        print(f"   ✓ Created: Ticket #{t.get('ticket_id')} - {t.get('title')}")
    else:
        print(f"   ✗ Failed: {ticket['title']}")

# 6. Get all tickets
print("\n6. Getting all tickets...")
response = requests.get(f"{BASE_URL}/tickets/", headers=headers)

if response.status_code == 200:
    tickets = response.json()
    print(f"✓ Found {len(tickets)} tickets:")
    for t in tickets:
        print(f"   - Ticket #{t['ticket_id']}: {t['title']} ({t['status']})")
else:
    print("✗ Failed:", response.text)

# 7. Get specific ticket
if len(tickets) > 0:
    print("\n7. Getting specific ticket...")
    ticket_id = tickets[0]['ticket_id']
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}", headers=headers)
    
    if response.status_code == 200:
        ticket = response.json()
        print(f"✓ Ticket #{ticket_id} details:")
        print(f"   Title: {ticket.get('title')}")
        print(f"   Description: {ticket.get('description')}")
        print(f"   Status: {ticket.get('status')}")
        print(f"   Priority: {ticket.get('priority')}")
    else:
        print("✗ Failed:", response.text)

# 8. Update ticket status
if len(tickets) > 0:
    print("\n8. Updating ticket status...")
    ticket_id = tickets[0]['ticket_id']
    update_data = {
        'status': 'in_progress'
    }
    response = requests.put(f"{BASE_URL}/tickets/{ticket_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        ticket = response.json()
        print(f"✓ Ticket #{ticket_id} updated!")
        print(f"   New Status: {ticket.get('status')}")
    else:
        print("✗ Failed:", response.text)

# 9. Get FAQ (if endpoint exists)
print("\n9. Getting FAQ...")
try:
    response = requests.get(f"{BASE_URL}/faq/", headers=headers)
    if response.status_code == 200:
        faqs = response.json()
        print(f"✓ Found {len(faqs)} FAQ entries:")
        for faq in faqs:
            print(f"   - Q: {faq.get('question')[:50]}...")
    else:
        print("   FAQ endpoint not available yet")
except:
    print("   FAQ endpoint not available")

# 10. Test analytics
print("\n10. Getting analytics...")
try:
    response = requests.get(f"{BASE_URL}/tickets/analytics", headers=headers)
    if response.status_code == 200:
        analytics = response.json()
        print("✓ Analytics retrieved:")
        print(f"   Total Tickets: {analytics.get('total_tickets')}")
        print(f"   Open Tickets: {analytics.get('open_tickets')}")
        print(f"   Resolved Tickets: {analytics.get('resolved_tickets')}")
    else:
        print("   Analytics endpoint not available")
except:
    print("   Analytics endpoint not available")

print("\n" + "=" * 60)
print("✓ Test suite complete!")
print("=" * 60)
print("\nTo run this script:")
print("1. Make sure the backend server is running")
print("2. Run: python test_api.py")
