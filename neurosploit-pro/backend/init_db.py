"""
Initialize database with a demo user
"""
import asyncio
import uuid
from sqlalchemy import select
from app.core.database import async_session_maker, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        # Check if admin user exists
        result = await session.execute(
            select(User).where(User.username == 'admin')
        )
        existing = result.scalar_one_or_none()
        if existing:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            username='admin',
            email='admin@example.com',
            hashed_password=get_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        session.add(admin)
        await session.commit()
        print("✅ Admin user created: admin / admin123")

if __name__ == '__main__':
    asyncio.run(init_db())
