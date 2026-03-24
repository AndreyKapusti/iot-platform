-- Создаем расширение для UUID (если понадобится)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
-- Таблица устройств (привязка к пользователю)
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_key VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, name)
);
CREATE INDEX idx_devices_api_key ON devices(api_key);
CREATE INDEX idx_devices_api_key ON devices(user_id);
-- =====================================================
-- Таблица для числовых показаний
-- =====================================================
CREATE TABLE IF NOT EXISTS sensor_metrics_numeric (
    id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW()
);
-- Индексы для числовых показаний
CREATE INDEX IF NOT EXISTS idx_numeric_device_time ON sensor_metrics_numeric(device_id, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_numeric_device_metric ON sensor_metrics_numeric(device_id, metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_numeric_metric_time ON sensor_metrics_numeric(metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_numeric_received_at ON sensor_metrics_numeric(received_at DESC);
-- =====================================================
-- Таблица для булевых показаний (motion, is_active, etc.)
-- =====================================================
CREATE TABLE IF NOT EXISTS sensor_metrics_boolean (
    id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value BOOLEAN NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW()
);
-- Индексы для булевых показаний
CREATE INDEX IF NOT EXISTS idx_boolean_device_time ON sensor_metrics_boolean(device_id, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_boolean_device_metric ON sensor_metrics_boolean(device_id, metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_boolean_metric_time ON sensor_metrics_boolean(metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_boolean_received_at ON sensor_metrics_boolean(received_at DESC);
CREATE INDEX IF NOT EXISTS idx_boolean_value ON sensor_metrics_boolean(device_id, metric_name, value)
WHERE value = true;
-- полезно для поиска активных событий
-- =====================================================
-- Таблица для строковых показаний
-- =====================================================
CREATE TABLE IF NOT EXISTS sensor_metrics_text (
    id BIGSERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW()
);
-- Индексы для строковых показаний
CREATE INDEX IF NOT EXISTS idx_text_device_time ON sensor_metrics_text(device_id, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_text_device_metric ON sensor_metrics_text(device_id, metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_text_metric_time ON sensor_metrics_text(metric_name, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_text_received_at ON sensor_metrics_text(received_at DESC);
-- B-tree индекс для точного поиска строк
CREATE INDEX IF NOT EXISTS idx_text_value ON sensor_metrics_text(metric_name, value)
WHERE value IS NOT NULL;
-- Комментарии к таблице и колонкам
COMMENT ON TABLE users IS 'Пользователи системы';
COMMENT ON COLUMN users.email IS 'Email пользователя (уникальный)';
COMMENT ON COLUMN users.username IS 'Имя пользователя (уникальное)';
COMMENT ON COLUMN users.hashed_password IS 'Хэш пароля';
COMMENT ON COLUMN users.is_active IS 'Активен ли пользователь';