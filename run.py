import subprocess
import sys
import time
import os

def run_command(cmd, wait=True):
    """Запускает команду"""
    try:
        print(f"🚀 Запуск: {cmd}")
        process = subprocess.Popen(cmd, shell=True)
        if wait:
            process.wait()
        return process
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    print("🎯 Запуск Client-Server приложения")
    
    # Запускаем сервер в фоне
    server_process = run_command(
        "python -m uvicorn server.src.main:app --reload --host 0.0.0.0 --port 8000",
        wait=False
    )
    
    if not server_process:
        return 1
    
    # Ждем запуска сервера
    time.sleep(3)
    
    # Запускаем клиент
    print("🖥️  Запуск клиента...")
    try:
        client_process = run_command("python client/src/main.py")
    except KeyboardInterrupt:
        print("\n👋 Остановка...")
    finally:
        # Останавливаем сервер
        print("⏹️  Остановка сервера...")
        server_process.terminate()
        server_process.wait()
        print("✅ Все процессы остановлены")

if __name__ == "__main__":
    main()