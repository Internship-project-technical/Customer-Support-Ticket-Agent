import os

# Your remote database details - UPDATE THIS WITH YOUR ACTUAL HOST!
REMOTE_HOST = input("Enter your remote database host (e.g., 192.168.1.100 or db.company.com): ").strip()
DB_USER = "root"
DB_PASSWORD = "Rev2005@!!"
DB_PORT = "3306"
DB_NAME = "ai_support_db"

print(f"\nConfiguring database connection to: {REMOTE_HOST}")

# Update .env file
env_content = f"""# Database Configuration
DB_HOST={REMOTE_HOST}
DB_PORT={DB_PORT}
DB_USER={DB_USER}
DB_PASSWORD={DB_PASSWORD}
DB_NAME={DB_NAME}
DATABASE_URL=mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{REMOTE_HOST}:{DB_PORT}/{DB_NAME}

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
import urllib.parse

# Remote database configuration
DB_HOST = "{REMOTE_HOST}"
DB_USER = "{DB_USER}"
DB_PASSWORD = "{DB_PASSWORD}"
DB_PORT = "{DB_PORT}"
DB_NAME = "{DB_NAME}"

# Encode password for special characters
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Build connection string
DATABASE_URL = f"mysql+pymysql://{{DB_USER}}:{{encoded_password}}@{{DB_HOST}}:{{DB_PORT}}/{{DB_NAME}}"

print(f"Connecting to remote database: {{DB_HOST}}:{{DB_PORT}}")

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

print("\n" + "="*60)
print("Configuration complete!")
print("="*60)
print(f"\nDatabase configured for: {REMOTE_HOST}")
print("You can now test the connection.")
