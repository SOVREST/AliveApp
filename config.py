import json
import os
import sys

def get_config_path():
    """Получить путь к файлу конфигурации рядом с exe/скриптом"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'aliveapp_config.json')

DEFAULT_CONFIG = {
    'programs': [],
    'interval_minutes': 5,
    'autostart': False
}

def load_config():
    """Загрузить конфигурацию из файла"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Убедимся что все ключи есть
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Сохранить конфигурацию в файл"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def add_program(config, name, path):
    """Добавить программу в список"""
    config['programs'].append({
        'name': name,
        'path': path,
        'enabled': True
    })
    return config

def remove_program(config, index):
    """Удалить программу из списка"""
    if 0 <= index < len(config['programs']):
        config['programs'].pop(index)
    return config

def toggle_program(config, index):
    """Включить/выключить мониторинг программы"""
    if 0 <= index < len(config['programs']):
        config['programs'][index]['enabled'] = not config['programs'][index]['enabled']
    return config
