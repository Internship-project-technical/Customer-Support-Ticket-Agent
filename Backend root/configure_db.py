import sys
import urllib.parse

print("=" * 60)
print("Database Connection Test")
print("=" * 60)

# Get remote host from user
print("\nPlease enter your remote database details:")
print("(The schema is already created on the remote server)\n")

remote_host = input("Remote MySQL Host (e.g., 192.168.1.100 or db.company.com): ").strip()
if not remote_host:
    print("✗ Host is required!")
    sys.exit(1)

db_user = input("Database Username [root]: ").strip() or "root"
db_password = input("Database Password [Geethu@17]: ").strip() or "Geethu@17"
db_port = input("Database Port [3306]: ").strip() or "3306"
db_name = input("Database Name [ai_support_db]: ").strip() or "ai_support_db"

print("\n" + "=" * 60)
print(f"Testing connection to: {remote_host}:{db_port}")
print("=" * 60)

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy import inspect
    
    # Encode password for special characters
    encoded_password = urllib.parse.quote_plus(db_password)
    database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{remote_host}:{db_port}/{db_name}"
    
    # Test connection
    engine = create_engine(database_url, pool_pre_ping=True)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print(f"\n✓ SUCCESS! Connected to MySQL {version}")
        
        # Show all databases
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
                print(f"\n✓ Found {len(tables)} tables in '{db_name}':")
                for table in tables:
                    # Get row count for each table
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = count_result.scalar()
                    print(f"  - {table}: {count} records")
            else:
                print(f"\n⚠ No tables found in '{db_name}'. You may need to create them.")
                print("  Run: python create_db.py to create tables")
        else:
            print(f"\n✗ Database '{db_name}' does not exist!")
            print("  Creating it now...")
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            print(f"✓ Database '{db_name}' created!")
        
        # Update configuration files
        print("\n" + "=" * 60)
        print("Updating configuration files...")
        print("=" * 60)
        
        # Update .env
        env_content = f"""# Database Configuration
DB_HOST={remote_host}
DB_PORT={db_port}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_NAME={db_name}
DATABASE_URL=mysql+pymysql://{db_user}:{db_password}@{remote_host}:{db_port}/{db_name}

# AI Service Configuration
LLAMA_BASE_URL=https://aimodels.jadeglobal.com:8082/ollama/api
LLAMA_MODEL=deepseek-coder:6.7b

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Updated .env file")
        
        # Update app/database.py
        database_content = f'''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Remote database configuration
DATABASE_URL = "mysql+pymysql://{db_user}:{db_password}@{remote_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        with open('app/database.py', 'w') as f:
            f.write(database_content)
        print("✓ Updated app/database.py")
        
        print("\n" + "=" * 60)
        print("✓ Configuration complete!")
        print("=" * 60)
        print("\nYou can now start your server:")
        print("  python -m uvicorn app.main:app --reload --port 8000")
        
except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nPlease check:")
    print("1. The remote host is correct and reachable")
    print("2. You have network access (VPN may be required)")
    print("3. MySQL is running on the remote server")
    print("4. Firewall allows port", db_port)
    print("5. The username and password are correct")
