import urllib.parse
import sys
import os

print("=" * 70)
print("Remote Database Connection Test")
print("=" * 70)

# Try to get host from .env file first
env_file = '.env'
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('DB_HOST='):
                host = line.split('=')[1].strip()
                print(f"Found configured host: {host}")
                break

# Ask for host if not found or override
remote_host = input("Enter remote MySQL host (IP or domain): ").strip()
if not remote_host:
    print("✗ Remote host is required!")
    sys.exit(1)

db_user = "root"
db_password = "Geethu@17"
db_port = "3306"
db_name = "ai_support_db"

print(f"\nTesting connection to: {remote_host}:{db_port}")
print("=" * 70)

try:
    from sqlalchemy import create_engine, text
    
    # Encode password
    encoded_password = urllib.parse.quote_plus(db_password)
    database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{remote_host}:{db_port}/{db_name}"
    
    print("\nAttempting to connect...")
    engine = create_engine(database_url, pool_pre_ping=True)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print(f"\n✓✓✓ SUCCESS! Connected to MySQL {version} ✓✓✓")
        print(f"✓ Server: {remote_host}:{db_port}")
        
        # Show available databases
        result = conn.execute(text("SHOW DATABASES"))
        databases = [row[0] for row in result.fetchall()]
        print(f"\nAvailable databases: {', '.join(databases)}")
        
        # Check if our database exists
        if db_name in databases:
            print(f"\n✓ Database '{db_name}' exists!")
            
            # Show tables
            conn.execute(text(f"USE {db_name}"))
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"\n✓ Found {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table}")
            else:
                print(f"\n⚠ No tables found in '{db_name}'")
        else:
            print(f"\n✗ Database '{db_name}' does not exist")
        
        print("\n" + "=" * 70)
        print("✓✓✓ Connection successful! ✓✓✓")
        print("=" * 70)
        
except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Verify the remote host is correct")
    print("2. Check if you need to connect to VPN")
    print("3. Make sure MySQL is running on the remote server")
    print("4. Check if firewall allows port 3306")
    print("5. Verify username and password are correct")
