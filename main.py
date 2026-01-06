"""
AliveApp - Мониторинг процессов
Автоматически перезапускает программы, если они закрылись
"""

import sys
import os

# Добавляем текущую директорию в путь
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import load_config, save_config
from monitor import ProcessMonitor
from tray import TrayIcon
from ui import MainWindow


class AliveApp:
    def __init__(self):
        self.config = load_config()
        self.monitor = None
        self.tray = None
        self.window = None

    def on_config_change(self, new_config, force_check=False):
        """Обработчик изменения конфига"""
        self.config = new_config
        if self.monitor:
            self.monitor.update_config(self.config)
            if force_check:
                self.monitor.trigger_check()

    def on_status_change(self, results):
        """Обработчик изменения статуса процессов"""
        if self.window:
            self.window.update_status(results)

        # Обновляем tooltip в трее
        if self.tray:
            running = sum(1 for _, status in results if status == 'running')
            total = len(results)
            self.tray.update_tooltip(f"AliveApp - {running}/{total} работает")

    def on_countdown(self, seconds):
        """Обработчик обратного отсчёта"""
        if self.window and self.window.root:
            self.window.root.after(0, lambda: self.window.update_countdown(seconds))

    def show_window(self):
        """Показать главное окно"""
        if self.window:
            self.window.show_window()

    def quit(self):
        """Выход из приложения"""
        if self.monitor:
            self.monitor.stop()
        if self.tray:
            self.tray.stop()
        if self.window and self.window.root:
            # Закрываем окно из главного потока tkinter
            try:
                self.window.root.after(0, self._shutdown)
            except:
                self._shutdown()
        else:
            self._shutdown()

    def _shutdown(self):
        """Завершение работы"""
        if self.window:
            self.window.quit()
        import os
        os._exit(0)

    def run(self):
        """Запустить приложение"""
        # Создаём монитор
        self.monitor = ProcessMonitor(
            self.config,
            on_status_change=self.on_status_change,
            on_countdown=self.on_countdown
        )
        self.monitor.start()

        # Создаём трей
        self.tray = TrayIcon(on_open=self.show_window, on_quit=self.quit)
        self.tray.start()

        # Создаём окно
        self.window = MainWindow(
            self.config,
            on_config_change=self.on_config_change,
            on_close=self.quit
        )

        root = self.window.create_window()

        # Сразу проверяем процессы
        self.monitor.check_and_start()

        # Запускаем главный цикл
        root.mainloop()


def main():
    app = AliveApp()
    app.run()


if __name__ == '__main__':
    main()
