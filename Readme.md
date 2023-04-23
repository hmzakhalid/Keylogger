# Minimal Keylogger
#### Author: [Hamza Khalid](https://github.com/hmzakhalid)

A simple, minimal, and efficient keylogger for Windows that doesn't require any external libraries. This keylogger uses the Windows API and low-level keyboard procedures to capture keystrokes and log them to a file.

## Features

- No external libraries required
- Uses Windows API and low-level keyboard procedures
- Runs in the background without displaying a console
- Start and stop the keylogger with keyboard shortcuts
- Automatically save logs at specified intervals
- Can be run from the command line with arguments

## How to use

1. Make sure you have Python 3.6 or later installed on your system.
2. Download or clone this repository.
3. Open a command prompt or terminal, navigate to the directory containing the keylogger, and run:

```bash
python run_keylogger.py <log_file> <save_interval>
```
 Replace `<log_file>` with the path of the file where you want to save the logs, and `<save_interval>` with the number of seconds between each automatic save.

For example:
```bash
python run_keylogger.py keylogger_output.txt 60
```

4. The keylogger will run in the background without showing a console. To start recording, press `CTRL + SHIFT + A`. To stop recording and exit the keylogger, press `CTRL + SHIFT + Z`.

## Notes

- This keylogger is for educational purposes only. Please use it responsibly and only on devices you have permission to monitor.
- As this keylogger uses low-level keyboard procedures, some antivirus software may detect it as a threat. Please be aware of this and use it only for educational purposes.




