import urllib.parse

print("=" * 70)
print("Remote Database Connection Test")
print("=" * 70)

# Get database host
remote_host = input("\nEnter the remote database host (IP or domain): ").strip()

if not remote_host:
    print("\n✗ No host entered!")
    exit(1)

db_user = "root"
db_password = "Rev2005@!!"
db_port = "3306"
db_name = "ai_support_db"

print(f"\nTesting connection to: {remote_host}:{db_port}")
print("=" * 70)

try:
    from sqlalchemy import create_engine, text

    # ✅ Encode password properly
    encoded_password = urllib.parse.quote_plus(db_password)

    # ✅ Correct DATABASE URL
    database_url = f"mysql+pymysql://{db_user}:{encoded_password}@{remote_host}:{db_port}/{db_name}"

    print("\nUsing DB URL:")
    print(database_url)  # debug

    print("\nAttempting to connect...")
    engine = create_engine(database_url, pool_pre_ping=True)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.scalar()

        print(f"\n✓✓✓ SUCCESS! Connected to MySQL {version} ✓✓✓")

        # ✅ IMPORTANT: Save ENCODED password in DATABASE_URL
        env_content = f"""# Database Configuration
DB_HOST={remote_host}
DB_PORT={db_port}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_NAME={db_name}
DATABASE_URL=mysql+pymysql://{db_user}:{encoded_password}@{remote_host}:{db_port}/{db_name}

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

        print("\n✓ Configuration saved to .env")

        print("\n" + "=" * 70)
        print("✓✓✓ Database configured successfully! ✓✓✓")
        print("=" * 70)
        print("\nStart your server:")
        print("  python -m uvicorn app.main:app --reload --port 8000")

except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("1. Wrong username/password ❗")
    print("2. Database does not exist ❗")
    print("3. MySQL service not running ❗")
    print("4. Host is incorrect ❗")