#!/usr/bin/env python3
"""
NeuroSploit v3 - Initialize Admin User
"""
import asyncio
import uuid
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.db.database import init_db, get_db, engine
from backend.core.security import get_password_hash
from backend.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


async def init_admin_user():
    """Initialize default admin user"""
    await init_db()
    
    async with AsyncSession(engine) as session:
        from sqlalchemy import select
        
        # Check if admin exists
        result = await session.execute(select(User).where(User.username == "admin"))
        admin_exists = result.scalar_one_or_none()
        
        if admin_exists:
            print("Admin user already exists!")
            print(f"Username: admin")
            print(f"Email: {admin_exists.email}")
            return
        
        # Create admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@neurosploit.local",
            hashed_password=get_password_hash("admin123!"),
            role="admin",
            is_active=True
        )
        
        session.add(admin_user)
        await session.commit()
        
        print("=" * 60)
        print("✓ Admin user created successfully!")
        print("=" * 60)
        print("Username: admin")
        print("Password: admin123!")
        print("Email: admin@neurosploit.local")
        print("Role: admin")
        print("=" * 60)
        print("⚠️  Please change the default password immediately!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(init_admin_user())
