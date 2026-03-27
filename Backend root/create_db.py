import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app import models

print("=" * 50)
print("Creating database tables...")
print("=" * 50)

# Create all tables
Base.metadata.create_all(bind=engine)

print("\n✓ Database tables created successfully!")
print("\nTables created:")
for table in Base.metadata.tables.keys():
    print(f"  - {table}")
