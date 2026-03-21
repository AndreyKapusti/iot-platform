#!/usr/bin/env python
"""
Скрипт для имитации отправки данных от Arduino на сервер.
Теперь с авторизацией через X-API-Key.
"""

import requests
import json
import time
import random
import argparse
from datetime import datetime, timezone
from typing import Dict, Any

class ArduinoSimulator:
    """Эмулятор Arduino с авторизацией по API-ключу"""
    
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key  # ← API-ключ для авторизации
        self.endpoint = f"{self.server_url}/api/v1/recive_data/"
    
    def generate_sensor_data(self, use_random: bool = True) -> Dict[str, Any]:
        """Генерирует показания датчиков"""
        if not use_random:
            return {
                "temperature": 23.5,
                "humidity": 60.0,
                "light": 450,
                "pressure": 1013.25,
                "co2": 420,
                "motion": False
            }
        
        return {
            "temperature": round(random.uniform(18.0, 28.0), 1),
            "humidity": round(random.uniform(40.0, 80.0), 1),
            "light": random.randint(100, 800),
            "pressure": round(random.uniform(1000, 1025), 1),
            "co2": random.randint(380, 500),
            "motion": random.choice([True, False])
        }
    
    def create_payload(self, sensors: Dict[str, Any]) -> Dict[str, Any]:
        """Создает полный payload для отправки"""
        return {
            "device_id": "arduino_simulator",  # device_id можно передавать, но сервер берет из api_key
            "temperature": sensors.get("temperature"),
            "humidity": sensors.get("humidity"),
            "light": sensors.get("light"),
            "pressure": sensors.get("pressure"),
            "co2": sensors.get("co2"),
            "motion": sensors.get("motion"),
            "device_timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "firmware": "2.1.0",
                "battery": random.randint(70, 100),
                "rssi": random.randint(-80, -40)
            }
        }
    
    def send_data(self, payload: Dict[str, Any]) -> bool:
        """Отправляет данные на сервер с API-ключом"""
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": self.api_key  # ← ключ в заголовке!
                },
                timeout=5
            )
            
            print(f"\n{'='*60}")
            print(f"📤 Отправлено на {self.endpoint}")
            print(f"{'='*60}")
            print(f"🔑 API Key: {self.api_key[:20]}...")  # показываем только начало
            print(f"📦 Payload:")
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            print(f"\n📨 Ответ сервера:")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   Body: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"   Error: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Ошибка: Не могу подключиться к серверу {self.server_url}")
            return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def run_continuous(self, interval: float = 1.0, count: int = None):
        """Непрерывная отправка данных"""
        print(f"🚀 Запуск симулятора Arduino")
        print(f"   API Key: {self.api_key[:20]}...")
        print(f"   Сервер: {self.server_url}")
        print(f"   Интервал: {interval} сек")
        print(f"   Нажмите Ctrl+C для остановки\n")
        
        sent_count = 0
        
        try:
            while True:
                sensors = self.generate_sensor_data(use_random=True)
                payload = self.create_payload(sensors)
                
                success = self.send_data(payload)
                sent_count += 1
                
                if success:
                    print(f"✅ Отправка #{sent_count} успешна")
                else:
                    print(f"❌ Отправка #{sent_count} не удалась")
                
                if count and sent_count >= count:
                    print(f"\n🏁 Достигнут лимит отправок ({count})")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Остановка. Всего отправлено: {sent_count}")
    
    def run_single(self):
        """Одиночная отправка"""
        sensors = self.generate_sensor_data(use_random=False)
        payload = self.create_payload(sensors)
        self.send_data(payload)


def main():
    parser = argparse.ArgumentParser(
        description="Симулятор Arduino с авторизацией по API-ключу"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        required=True,  # ← API-ключ обязателен!
        help="API-ключ устройства (получить через POST /api/v1/devices)"
    )
    
    parser.add_argument(
        "--url", "-u",
        default="http://localhost:8000",
        help="URL сервера (по умолчанию: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="Непрерывная отправка"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=1.0,
        help="Интервал между отправками (сек)"
    )
    
    parser.add_argument(
        "--count", "-n",
        type=int,
        help="Количество отправок"
    )
    
    args = parser.parse_args()
    
    simulator = ArduinoSimulator(args.url, args.api_key)
    
    if args.continuous:
        simulator.run_continuous(interval=args.interval, count=args.count)
    else:
        simulator.run_single()


if __name__ == "__main__":
    main()