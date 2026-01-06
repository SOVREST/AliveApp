import pystray
from PIL import Image, ImageDraw
import threading

class TrayIcon:
    def __init__(self, on_open=None, on_quit=None):
        self.on_open = on_open
        self.on_quit = on_quit
        self.icon = None
        self.thread = None

    def create_icon_image(self):
        """Создать иконку пера"""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Перо (стилизованное)
        # Основа пера - наклонённый овал
        draw.polygon([
            (48, 8),   # верхний кончик
            (52, 16),  # правый изгиб
            (20, 52),  # нижняя часть справа
            (12, 56),  # кончик пера (низ)
            (8, 52),   # нижняя часть слева
            (44, 12),  # левый изгиб
        ], fill=(70, 130, 180, 255), outline=(50, 100, 150, 255), width=1)

        # Стержень пера
        draw.line([(12, 56), (6, 62)], fill=(139, 69, 19, 255), width=3)

        # Блик на пере
        draw.line([(42, 18), (24, 42)], fill=(135, 180, 220, 255), width=2)

        return image

    def open_window(self, icon, item):
        """Обработчик открытия окна"""
        if self.on_open:
            self.on_open()

    def quit_app(self, icon, item):
        """Обработчик выхода"""
        icon.stop()
        if self.on_quit:
            self.on_quit()

    def create_menu(self):
        """Создать меню трея"""
        return pystray.Menu(
            pystray.MenuItem('Открыть', self.open_window, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Выход', self.quit_app)
        )

    def run(self):
        """Запустить иконку в трее"""
        image = self.create_icon_image()
        menu = self.create_menu()

        self.icon = pystray.Icon(
            'AliveApp',
            image,
            'AliveApp - Мониторинг процессов',
            menu
        )

        self.icon.run()

    def start(self):
        """Запустить в отдельном потоке"""
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        """Остановить иконку"""
        if self.icon:
            self.icon.stop()

    def update_tooltip(self, text):
        """Обновить подсказку"""
        if self.icon:
            self.icon.title = text
