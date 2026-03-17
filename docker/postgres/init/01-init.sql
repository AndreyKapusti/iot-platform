-- Создаем расширение для UUID (если понадобится)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Создаем таблицу пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
-- Создаем индекс для быстрого поиска по email
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
-- Комментарии к таблице и колонкам
COMMENT ON TABLE users IS 'Пользователи системы';
COMMENT ON COLUMN users.email IS 'Email пользователя (уникальный)';
COMMENT ON COLUMN users.username IS 'Имя пользователя (уникальное)';
COMMENT ON COLUMN users.hashed_password IS 'Хэш пароля';
COMMENT ON COLUMN users.is_active IS 'Активен ли пользователь';
-- Создаем тестового пользователя (пароль: "password" - заменим на хэш позже)
-- Пока закомментировано, добавим через код
-- INSERT INTO users (email, username, hashed_password) 
-- VALUES ('test@test.com', 'testuser', 'fake_hash_will_replace_later');