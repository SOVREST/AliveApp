import os
import sys

def get_startup_folder():
    """Получить путь к папке автозагрузки"""
    return os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

def get_shortcut_path():
    """Получить путь к ярлыку"""
    return os.path.join(get_startup_folder(), 'AliveApp.lnk')

def get_exe_path():
    """Получить путь к текущему exe/скрипту"""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(sys.argv[0])

def is_autostart_enabled():
    """Проверить, включен ли автозапуск"""
    return os.path.exists(get_shortcut_path())

def enable_autostart():
    """Включить автозапуск"""
    try:
        import winshell
        from win32com.client import Dispatch

        shortcut_path = get_shortcut_path()
        target = get_exe_path()

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.Description = "AliveApp - Process Monitor"
        shortcut.save()
        return True
    except ImportError:
        # Если нет winshell, создаём через PowerShell
        return enable_autostart_powershell()
    except Exception as e:
        print(f"Ошибка создания ярлыка: {e}")
        return False

def enable_autostart_powershell():
    """Создать ярлык через PowerShell"""
    import subprocess

    shortcut_path = get_shortcut_path()
    target = get_exe_path()
    work_dir = os.path.dirname(target)

    ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{target}"
$Shortcut.WorkingDirectory = "{work_dir}"
$Shortcut.Description = "AliveApp - Process Monitor"
$Shortcut.Save()
'''

    try:
        subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return os.path.exists(shortcut_path)
    except Exception as e:
        print(f"Ошибка PowerShell: {e}")
        return False

def disable_autostart():
    """Выключить автозапуск"""
    shortcut_path = get_shortcut_path()
    try:
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        return True
    except Exception as e:
        print(f"Ошибка удаления ярлыка: {e}")
        return False

def set_autostart(enabled):
    """Установить состояние автозапуска"""
    if enabled:
        return enable_autostart()
    else:
        return disable_autostart()
