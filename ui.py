import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import webbrowser

GITHUB_URL = "https://github.com/SOVREST/AliveApp"
AUTHOR_URL = "https://sovrest.com"

# Переводы
TRANSLATIONS = {
    'en': {
        'window_title': 'AliveApp - Process Monitor',
        'programs_list': 'Programs to monitor',
        'name': 'Name',
        'path': 'Path',
        'status': 'Status',
        'add': 'Add',
        'remove': 'Remove',
        'toggle': 'On/Off',
        'check_now': 'Check Now',
        'statistics': 'Statistics',
        'checks': 'Checks',
        'starts': 'Starts',
        'next_check': 'Next check',
        'show': 'Show',
        'settings': 'Settings',
        'interval': 'Check interval (min):',
        'autostart': 'Start with Windows',
        'ready': 'Ready',
        'enabled': 'Enabled',
        'disabled': 'Disabled',
        'running': 'Running',
        'started': 'Started',
        'failed': 'Failed',
        'not_found': 'Not found',
        'select_program': 'Select program',
        'exe_files': 'Executable files',
        'all_files': 'All files',
        'program_name': 'Program name',
        'enter_name': 'Enter name:',
        'ok': 'OK',
        'warning': 'Warning',
        'select_to_remove': 'Select a program to remove',
        'select_program_toggle': 'Select a program',
        'confirm': 'Confirm',
        'remove_confirm': "Remove '{}' from list?",
        'added': 'Added',
        'removed': 'Removed',
        'monitoring_on': 'Monitoring enabled',
        'monitoring_off': 'Monitoring disabled',
        'autostart_on': 'Autostart enabled',
        'autostart_off': 'Autostart disabled',
        'error': 'Error',
        'autostart_error': 'Failed to change autostart',
        'created_by': 'created',
    },
    'ru': {
        'window_title': 'AliveApp - Мониторинг процессов',
        'programs_list': 'Список программ для мониторинга',
        'name': 'Название',
        'path': 'Путь',
        'status': 'Статус',
        'add': 'Добавить',
        'remove': 'Удалить',
        'toggle': 'Вкл/Выкл',
        'check_now': 'Проверить сейчас',
        'statistics': 'Статистика',
        'checks': 'Проверок',
        'starts': 'Запусков',
        'next_check': 'До проверки',
        'show': 'Показывать',
        'settings': 'Настройки',
        'interval': 'Интервал проверки (мин):',
        'autostart': 'Запускать с Windows',
        'ready': 'Готов',
        'enabled': 'Включено',
        'disabled': 'Выключено',
        'running': 'Работает',
        'started': 'Запущено',
        'failed': 'Ошибка',
        'not_found': 'Не найден',
        'select_program': 'Выберите программу',
        'exe_files': 'Исполняемые файлы',
        'all_files': 'Все файлы',
        'program_name': 'Название программы',
        'enter_name': 'Введите название:',
        'ok': 'OK',
        'warning': 'Внимание',
        'select_to_remove': 'Выберите программу для удаления',
        'select_program_toggle': 'Выберите программу',
        'confirm': 'Подтверждение',
        'remove_confirm': "Удалить '{}' из списка?",
        'added': 'Добавлено',
        'removed': 'Удалено',
        'monitoring_on': 'Мониторинг включен',
        'monitoring_off': 'Мониторинг выключен',
        'autostart_on': 'Автозапуск включен',
        'autostart_off': 'Автозапуск выключен',
        'error': 'Ошибка',
        'autostart_error': 'Не удалось изменить автозапуск',
        'created_by': 'создано',
    }
}


class MainWindow:
    def __init__(self, config, on_config_change=None, on_close=None):
        self.config = config
        self.on_config_change = on_config_change
        self.on_close = on_close

        self.root = None
        self.tree = None
        self.interval_var = None
        self.autostart_var = None
        self.show_countdown_var = None

        # Язык (по умолчанию английский)
        self.lang = self.config.get('language', 'en')

        # Статистика
        self.stats = {
            'total_checks': 0,
            'total_starts': 0
        }

        # Обратный отсчёт
        self.countdown_seconds = 0
        self.countdown_label = None
        self.countdown_frame = None

        # Ссылки на виджеты для обновления языка
        self.widgets = {}

    def t(self, key):
        """Получить перевод"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS['en']).get(key, key)

    def create_window(self):
        """Создать главное окно"""
        self.root = tk.Tk()
        self.root.title(self.t('window_title'))
        self.root.geometry("600x550")
        self.root.minsize(500, 450)

        # Устанавливаем иконку пера программно
        self.set_window_icon()

        # При закрытии - сворачиваем в трей
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.create_widgets()
        self.load_data()

        return self.root

    def set_window_icon(self):
        """Установить иконку окна (перо)"""
        try:
            from PIL import Image, ImageTk, ImageDraw

            # Создаём иконку пера
            size = 32
            image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # Перо (стилизованное) - уменьшенная версия
            draw.polygon([
                (24, 4),
                (26, 8),
                (10, 26),
                (6, 28),
                (4, 26),
                (22, 6),
            ], fill=(70, 130, 180, 255), outline=(50, 100, 150, 255), width=1)
            draw.line([(6, 28), (3, 31)], fill=(139, 69, 19, 255), width=2)

            photo = ImageTk.PhotoImage(image)
            self.root.iconphoto(True, photo)
            self._icon_photo = photo  # Сохраняем ссылку
        except Exception as e:
            pass

    def create_widgets(self):
        """Создать виджеты"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок и ссылки
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        self.widgets['title'] = ttk.Label(header_frame, text=self.t('programs_list'), font=('Segoe UI', 11, 'bold'))
        self.widgets['title'].pack(side=tk.LEFT)

        # Кнопка смены языка
        self.lang_btn = ttk.Button(header_frame, text="RU" if self.lang == 'en' else "EN", width=3, command=self.toggle_language)
        self.lang_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # GitHub ссылка
        if GITHUB_URL:
            github_link = ttk.Label(header_frame, text="GitHub", foreground='blue', cursor='hand2', font=('Segoe UI', 9, 'underline'))
            github_link.pack(side=tk.RIGHT, padx=(5, 0))
            github_link.bind('<Button-1>', lambda e: webbrowser.open(GITHUB_URL))

        # SOVREST.COM ссылка
        if AUTHOR_URL:
            author_link = ttk.Label(header_frame, text=f"{self.t('created_by')} SOVREST.COM", foreground='gray', cursor='hand2', font=('Segoe UI', 8))
            author_link.pack(side=tk.RIGHT, padx=(10, 0))
            author_link.bind('<Button-1>', lambda e: webbrowser.open(AUTHOR_URL))
            self.widgets['author'] = author_link

        # Таблица программ
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('name', 'path', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')

        self.tree.heading('name', text=self.t('name'))
        self.tree.heading('path', text=self.t('path'))
        self.tree.heading('status', text=self.t('status'))

        self.tree.column('name', width=150, minwidth=100)
        self.tree.column('path', width=300, minwidth=200)
        self.tree.column('status', width=100, minwidth=80)

        # Скроллбар
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки управления
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        self.widgets['add_btn'] = ttk.Button(btn_frame, text=self.t('add'), command=self.add_program)
        self.widgets['add_btn'].pack(side=tk.LEFT, padx=(0, 5))

        self.widgets['remove_btn'] = ttk.Button(btn_frame, text=self.t('remove'), command=self.remove_program)
        self.widgets['remove_btn'].pack(side=tk.LEFT, padx=(0, 5))

        self.widgets['toggle_btn'] = ttk.Button(btn_frame, text=self.t('toggle'), command=self.toggle_program)
        self.widgets['toggle_btn'].pack(side=tk.LEFT, padx=(0, 5))

        self.widgets['check_btn'] = ttk.Button(btn_frame, text=self.t('check_now'), command=self.check_now)
        self.widgets['check_btn'].pack(side=tk.RIGHT)

        # Статистика
        self.widgets['stats_frame'] = ttk.LabelFrame(main_frame, text=self.t('statistics'), padding="10")
        self.widgets['stats_frame'].pack(fill=tk.X, pady=(15, 0))

        stats_inner = ttk.Frame(self.widgets['stats_frame'])
        stats_inner.pack(fill=tk.X)

        self.checks_label = ttk.Label(stats_inner, text=f"{self.t('checks')}: 0")
        self.checks_label.pack(side=tk.LEFT, padx=(0, 20))

        self.starts_label = ttk.Label(stats_inner, text=f"{self.t('starts')}: 0")
        self.starts_label.pack(side=tk.LEFT)

        # Обратный отсчёт
        self.countdown_frame = ttk.Frame(self.widgets['stats_frame'])
        self.countdown_frame.pack(fill=tk.X, pady=(5, 0))

        self.countdown_label = ttk.Label(self.countdown_frame, text=f"{self.t('next_check')}: --:--", font=('Segoe UI', 9))
        self.countdown_label.pack(side=tk.LEFT)

        self.show_countdown_var = tk.BooleanVar(value=self.config.get('show_countdown', True))
        self.widgets['countdown_check'] = ttk.Checkbutton(
            self.countdown_frame,
            text=self.t('show'),
            variable=self.show_countdown_var,
            command=self.toggle_countdown_visibility
        )
        self.widgets['countdown_check'].pack(side=tk.RIGHT)

        # Применяем видимость
        self.toggle_countdown_visibility()

        # Настройки
        self.widgets['settings_frame'] = ttk.LabelFrame(main_frame, text=self.t('settings'), padding="10")
        self.widgets['settings_frame'].pack(fill=tk.X, pady=(10, 0))

        # Интервал
        interval_frame = ttk.Frame(self.widgets['settings_frame'])
        interval_frame.pack(fill=tk.X, pady=(0, 5))

        self.widgets['interval_label'] = ttk.Label(interval_frame, text=self.t('interval'))
        self.widgets['interval_label'].pack(side=tk.LEFT)

        self.interval_var = tk.StringVar(value=str(self.config.get('interval_minutes', 5)))
        interval_spin = ttk.Spinbox(
            interval_frame,
            from_=1,
            to=60,
            width=5,
            textvariable=self.interval_var,
            command=self.save_settings
        )
        interval_spin.pack(side=tk.LEFT, padx=(10, 0))
        interval_spin.bind('<FocusOut>', lambda e: self.save_settings())

        # Автозапуск
        self.autostart_var = tk.BooleanVar(value=self.config.get('autostart', False))
        self.widgets['autostart_check'] = ttk.Checkbutton(
            self.widgets['settings_frame'],
            text=self.t('autostart'),
            variable=self.autostart_var,
            command=self.toggle_autostart
        )
        self.widgets['autostart_check'].pack(anchor=tk.W)

        # Статус бар
        self.status_var = tk.StringVar(value=self.t('ready'))
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def toggle_language(self):
        """Переключить язык"""
        self.lang = 'ru' if self.lang == 'en' else 'en'
        self.config['language'] = self.lang
        self.save_config()

        # Обновляем кнопку
        self.lang_btn.config(text="RU" if self.lang == 'en' else "EN")

        # Обновляем заголовок окна
        self.root.title(self.t('window_title'))

        # Обновляем виджеты
        self.widgets['title'].config(text=self.t('programs_list'))
        self.widgets['add_btn'].config(text=self.t('add'))
        self.widgets['remove_btn'].config(text=self.t('remove'))
        self.widgets['toggle_btn'].config(text=self.t('toggle'))
        self.widgets['check_btn'].config(text=self.t('check_now'))
        self.widgets['stats_frame'].config(text=self.t('statistics'))
        self.widgets['settings_frame'].config(text=self.t('settings'))
        self.widgets['interval_label'].config(text=self.t('interval'))
        self.widgets['autostart_check'].config(text=self.t('autostart'))
        self.widgets['countdown_check'].config(text=self.t('show'))

        if 'author' in self.widgets:
            self.widgets['author'].config(text=f"{self.t('created_by')} SOVREST.COM")

        # Обновляем заголовки таблицы
        self.tree.heading('name', text=self.t('name'))
        self.tree.heading('path', text=self.t('path'))
        self.tree.heading('status', text=self.t('status'))

        # Обновляем статистику
        self.checks_label.config(text=f"{self.t('checks')}: {self.stats['total_checks']}")
        self.starts_label.config(text=f"{self.t('starts')}: {self.stats['total_starts']}")

        # Обновляем статус
        self.status_var.set(self.t('ready'))

        # Перезагружаем данные таблицы
        self.load_data()

    def toggle_countdown_visibility(self):
        """Переключить видимость обратного отсчёта"""
        if self.show_countdown_var.get():
            self.countdown_label.pack(side=tk.LEFT)
        else:
            self.countdown_label.pack_forget()

        self.config['show_countdown'] = self.show_countdown_var.get()
        self.save_config()

    def update_countdown(self, seconds):
        """Обновить обратный отсчёт"""
        self.countdown_seconds = seconds
        if self.countdown_label and self.show_countdown_var.get():
            minutes = seconds // 60
            secs = seconds % 60
            self.countdown_label.config(text=f"{self.t('next_check')}: {minutes:02d}:{secs:02d}")

    def update_stats(self, checks=0, starts=0):
        """Обновить статистику"""
        self.stats['total_checks'] += checks
        self.stats['total_starts'] += starts

        if self.checks_label:
            self.checks_label.config(text=f"{self.t('checks')}: {self.stats['total_checks']}")
        if self.starts_label:
            self.starts_label.config(text=f"{self.t('starts')}: {self.stats['total_starts']}")

    def check_now(self):
        """Принудительная проверка"""
        if self.on_config_change:
            self.on_config_change(self.config, force_check=True)

    def load_data(self):
        """Загрузить данные в таблицу"""
        # Очистить
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнить
        for prog in self.config.get('programs', []):
            status = self.t('enabled') if prog.get('enabled', True) else self.t('disabled')
            self.tree.insert('', tk.END, values=(prog['name'], prog['path'], status))

    def add_program(self):
        """Добавить программу"""
        file_path = filedialog.askopenfilename(
            title=self.t('select_program'),
            filetypes=[(self.t('exe_files'), "*.exe"), (self.t('all_files'), "*.*")]
        )

        if file_path:
            name = os.path.splitext(os.path.basename(file_path))[0]

            # Диалог для имени
            dialog = tk.Toplevel(self.root)
            dialog.title(self.t('program_name'))
            dialog.geometry("300x100")
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(dialog, text=self.t('enter_name')).pack(pady=(10, 5))

            name_var = tk.StringVar(value=name)
            name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
            name_entry.pack(pady=5)
            name_entry.select_range(0, tk.END)
            name_entry.focus()

            def save():
                final_name = name_var.get().strip() or name
                self.config['programs'].append({
                    'name': final_name,
                    'path': file_path,
                    'enabled': True
                })
                self.save_config()
                self.load_data()
                dialog.destroy()
                self.status_var.set(f"{self.t('added')}: {final_name}")

            ttk.Button(dialog, text=self.t('ok'), command=save).pack(pady=5)
            dialog.bind('<Return>', lambda e: save())

    def remove_program(self):
        """Удалить выбранную программу"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.t('warning'), self.t('select_to_remove'))
            return

        index = self.tree.index(selection[0])
        name = self.config['programs'][index]['name']

        if messagebox.askyesno(self.t('confirm'), self.t('remove_confirm').format(name)):
            self.config['programs'].pop(index)
            self.save_config()
            self.load_data()
            self.status_var.set(f"{self.t('removed')}: {name}")

    def toggle_program(self):
        """Включить/выключить мониторинг программы"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.t('warning'), self.t('select_program_toggle'))
            return

        index = self.tree.index(selection[0])
        self.config['programs'][index]['enabled'] = not self.config['programs'][index].get('enabled', True)
        self.save_config()
        self.load_data()

        status = self.t('monitoring_on') if self.config['programs'][index]['enabled'] else self.t('monitoring_off')
        self.status_var.set(f"{status}: {self.config['programs'][index]['name']}")

    def save_settings(self):
        """Сохранить настройки интервала"""
        try:
            interval = int(self.interval_var.get())
            if 1 <= interval <= 60:
                self.config['interval_minutes'] = interval
                self.save_config()
        except ValueError:
            pass

    def toggle_autostart(self):
        """Переключить автозапуск"""
        from autostart import set_autostart

        enabled = self.autostart_var.get()
        success = set_autostart(enabled)

        if success:
            self.config['autostart'] = enabled
            self.save_config()
            status = self.t('autostart_on') if enabled else self.t('autostart_off')
            self.status_var.set(status)
        else:
            self.autostart_var.set(not enabled)
            messagebox.showerror(self.t('error'), self.t('autostart_error'))

    def save_config(self):
        """Сохранить конфиг и уведомить"""
        from config import save_config
        save_config(self.config)

        if self.on_config_change:
            self.on_config_change(self.config)

    def update_status(self, results):
        """Обновить статусы в таблице"""
        if not self.root or not self.tree:
            return

        # Обновляем через главный поток tkinter
        def update():
            items = self.tree.get_children()
            starts_count = 0
            for i, (name, status) in enumerate(results):
                if status == 'started':
                    starts_count += 1
                if i < len(items):
                    current = self.tree.item(items[i])['values']
                    status_text = {
                        'running': self.t('running'),
                        'started': self.t('started'),
                        'failed': self.t('failed'),
                        'not_found': self.t('not_found'),
                        'disabled': self.t('disabled')
                    }.get(status, status)
                    self.tree.item(items[i], values=(current[0], current[1], status_text))

            # Обновляем статистику
            self.update_stats(checks=1, starts=starts_count)

        if self.root:
            self.root.after(0, update)

    def show_window(self):
        """Показать окно"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

    def hide_window(self):
        """Скрыть окно в трей"""
        if self.root:
            self.root.withdraw()

    def quit(self):
        """Закрыть приложение"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
            self.root = None
