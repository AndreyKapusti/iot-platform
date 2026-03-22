import psycopg
from psycopg_pool import AsyncConnectionPool
from fastapi import HTTPException
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool: Optional[AsyncConnectionPool] = None
    
    async def connect(self):
        """Создание пула подключений к БД"""
        try:
            self.pool = AsyncConnectionPool(
                "postgresql://iot_user:iot_password@localhost:5432/iot_platform",
                min_size=5,
                max_size=20,
                open=False  # не открывать сразу
            )
            await self.pool.open()
            logger.info("✅ Подключение к БД установлено (psycopg)")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к БД: {e}")
            raise
    
    async def disconnect(self):
        """Закрытие пула подключений"""
        if self.pool:
            await self.pool.close()
            logger.info("🔌 Подключение к БД закрыто")
    
    async def fetch_one(self, query: str, *args):
        """Получить одну запись"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                row = await cur.fetchone()
                if row:
                    # Преобразуем Record в словарь
                    columns = [desc.name for desc in cur.description]
                    return dict(zip(columns, row))
                return None
    
    async def fetch_all(self, query: str, *args):
        """Получить все записи"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                rows = await cur.fetchall()
                if rows and cur.description:
                    columns = [desc.name for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
                return []
    
    async def execute(self, query: str, *args):
        """Выполнить запрос (INSERT, UPDATE, DELETE)"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                return str(cur.rowcount)
    
    async def fetch_val(self, query: str, *args):
        """Получить одно значение"""
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                row = await cur.fetchone()
                return row[0] if row else None

# Создаем глобальный экземпляр БД
db = Database()