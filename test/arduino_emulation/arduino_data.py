import random
import requests
import time
import argparse
from datetime import datetime, timezone
from typing import Dict, Any

class ArduinoSimulator:
    """Эмулятор Arduino с авторизацией по API-ключу и новым форматом данных"""
    
    def __init__(self, server_url: str, api_key: str, device_id: int):
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.device_id = device_id  # теперь это int
        self.endpoint = f"{self.server_url}/api/v1/receive_data/"
    
    def generate_readings(self, use_random: bool = True) -> Dict[str, Any]:
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
            "motion": random.choice([True, False]),
            "test_int": random.randint(100, 800),
            "test_bool": random.choice([True, False]),
            "test_str": random.choice(['a', 'b', 'c', 'd'])
        }
    
    def generate_metadata(self) -> Dict[str, Any]:
        """Генерирует метаданные устройства"""
        return {
            "firmware": "2.1.0",
            "battery": random.randint(70, 100),
            "rssi": random.randint(-80, -40)
        }
    
    def create_payload(self, readings: Dict[str, Any]) -> Dict[str, Any]:
        """Создает полный payload в новом формате"""
        return {
            "device_id": self.device_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "readings": readings,
            "metadata": self.generate_metadata()
        }
    
    def send_data(self, payload: Dict[str, Any]) -> bool:
        """Отправляет данные на сервер"""
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": self.api_key
                },
                timeout=5
            )
            
            print(f"\n{'='*60}")
            print(f"📤 Отправлено на {self.endpoint}")
            print(f"{'='*60}")
            print(f"🔑 API Key: {self.api_key[:20]}...")
            print(f"📦 Payload:")
            import json
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
        print(f"   Device ID: {self.device_id}")
        print(f"   API Key: {self.api_key[:20]}...")
        print(f"   Сервер: {self.server_url}")
        print(f"   Интервал: {interval} сек")
        print(f"   Нажмите Ctrl+C для остановки\n")
        
        sent_count = 0
        
        try:
            while True:
                readings = self.generate_readings(use_random=True)
                payload = self.create_payload(readings)
                
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
        readings = self.generate_readings(use_random=False)
        payload = self.create_payload(readings)
        self.send_data(payload)


def main():
    parser = argparse.ArgumentParser(
        description="Симулятор Arduino с новым форматом данных"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        required=True,
        help="API-ключ устройства"
    )
    
    parser.add_argument(
        "--device-id", "-d",
        type=int,
        required=True,
        help="ID устройства (число)"
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
    
    simulator = ArduinoSimulator(args.url, args.api_key, args.device_id)
    
    if args.continuous:
        simulator.run_continuous(interval=args.interval, count=args.count)
    else:
        simulator.run_single()


if __name__ == "__main__":
    main()