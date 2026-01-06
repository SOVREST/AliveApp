# AliveApp

A lightweight Windows process monitor that automatically restarts applications if they close unexpectedly.

## Features

- **Process Monitoring** - Continuously monitors specified applications
- **Auto-Restart** - Automatically restarts programs when they close
- **System Tray** - Runs quietly in the system tray with a feather icon
- **Statistics** - Tracks total checks and restart counts
- **Countdown Timer** - Shows time until next check (toggleable)
- **Windows Autostart** - Option to run at Windows startup
- **Multilingual** - English and Russian interface (switchable)

## Screenshot

![AliveApp Screenshot](screenshot.png)

## Installation

### Option 1: Download Release
Download the latest `AliveApp.exe` from [Releases](https://github.com/SOVREST/AliveApp/releases).

### Option 2: Run from Source

1. Clone the repository:
```bash
git clone https://github.com/SOVREST/AliveApp.git
cd AliveApp
```

2. Install dependencies:
```bash
pip install psutil pystray pillow
```

3. Run:
```bash
python main.py
```

## Building Executable

To build a standalone executable:

```bash
pip install pyinstaller
python create_icon.py
pyinstaller --onefile --windowed --name AliveApp --icon=icon.ico main.py
```

The executable will be created in the `dist` folder.

## Usage

1. Launch AliveApp
2. Click "Add" to add programs you want to monitor
3. Set the check interval (1-60 minutes)
4. Enable "Run at Windows startup" if desired
5. Minimize to system tray

The application will automatically restart any monitored programs that close.

## Configuration

Settings are stored in `config.json` in the application directory:

```json
{
  "programs": [
    {
      "name": "MyApp",
      "path": "C:\\Path\\To\\MyApp.exe",
      "enabled": true
    }
  ],
  "interval_minutes": 5,
  "autostart": false,
  "language": "en"
}
```

## Requirements

- Windows 10/11
- Python 3.8+ (if running from source)

## Dependencies

- `psutil` - Process management
- `pystray` - System tray icon
- `pillow` - Icon generation
- `tkinter` - GUI (included with Python)

## License

MIT License

## Author

Created by [SOVREST.COM](https://sovrest.com)

## Links

- [GitHub Repository](https://github.com/SOVREST/AliveApp)
- [Report Issues](https://github.com/SOVREST/AliveApp/issues)
