import psutil
import subprocess
import threading
import time
import os

class ProcessMonitor:
    def __init__(self, config, on_status_change=None, on_countdown=None):
        self.config = config
        self.on_status_change = on_status_change
        self.on_countdown = on_countdown
        self.running = False
        self.thread = None
        self.force_check = False

    def is_process_running(self, exe_path):
        """Проверить, запущен ли процесс по пути к exe"""
        exe_name = os.path.basename(exe_path).lower()
        try:
            for proc in psutil.process_iter(['name', 'exe']):
                try:
                    proc_name = proc.info['name']
                    proc_exe = proc.info['exe']

                    # Сначала проверяем по полному пути
                    if proc_exe and os.path.normcase(proc_exe) == os.path.normcase(exe_path):
                        return True

                    # Если путь недоступен, проверяем по имени
                    if proc_name and proc_name.lower() == exe_name:
                        return True

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass
        return False

    def start_process(self, exe_path):
        """Запустить процесс"""
        try:
            if os.path.exists(exe_path):
                # Запускаем в рабочей директории программы
                work_dir = os.path.dirname(exe_path)
                subprocess.Popen(
                    exe_path,
                    cwd=work_dir,
                    shell=False,
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
                )
                return True
        except Exception as e:
            print(f"Ошибка запуска {exe_path}: {e}")
        return False

    def check_and_start(self):
        """Проверить все программы и запустить незапущенные"""
        results = []
        for prog in self.config.get('programs', []):
            if not prog.get('enabled', True):
                results.append((prog['name'], 'disabled'))
                continue

            path = prog.get('path', '')
            name = prog.get('name', os.path.basename(path))

            if not path or not os.path.exists(path):
                results.append((name, 'not_found'))
                continue

            is_running = self.is_process_running(path)

            if is_running:
                results.append((name, 'running'))
            else:
                started = self.start_process(path)
                results.append((name, 'started' if started else 'failed'))

        if self.on_status_change:
            self.on_status_change(results)

        return results

    def monitor_loop(self):
        """Основной цикл мониторинга"""
        while self.running:
            self.check_and_start()

            # Ждём интервал, но проверяем флаг каждую секунду
            interval = self.config.get('interval_minutes', 5) * 60
            for remaining in range(interval, 0, -1):
                if not self.running:
                    break
                if self.force_check:
                    self.force_check = False
                    break

                # Обновляем обратный отсчёт
                if self.on_countdown:
                    self.on_countdown(remaining)

                time.sleep(1)

    def trigger_check(self):
        """Принудительная проверка"""
        self.force_check = True

    def start(self):
        """Запустить мониторинг в фоновом потоке"""
        if self.thread and self.thread.is_alive():
            return

        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Остановить мониторинг"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def update_config(self, config):
        """Обновить конфигурацию"""
        self.config = config
