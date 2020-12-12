import ctypes
import time
import os
import signal
import psutil


from ctypes import wintypes
from plyer import notification

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def get_pid():
    user32 = ctypes.windll.user32

    h_wnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
    #print(pid.value)
    return pid.value

def generate_msg():
    notification.notify(
            title="Message",
            message="Suspicious Activity Detected",
            timeout=10
            )


class FoundWindow(Exception):
  pass

def titleExists(title):
  status = []
  def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
      length = GetWindowTextLength(hwnd)
      buff = ctypes.create_unicode_buffer(length + 1)
      GetWindowText(hwnd, buff, length + 1)
      if buff.value == title:
        status.append(True)
      return True
  EnumWindows(EnumWindowsProc(foreach_window), 0)
  return len(status) > 0

threshold_point=0

while True:
  ls = ["dummy - Notepad","Cyber_Project Sem-5"]
  for i in ls:
    if titleExists(i):
      print('Suspicious Activity detected')
      pid_value = get_pid()
      print(pid_value)
      p = psutil.Process(pid_value)
      p.terminate()
      generate_msg()
      threshold_point+=1
      if threshold_point>=5:
          os.system("shutdown /s /t 1")
      #os.kill(pid_value, signal.SIGTERM)
      #os.system("shutdown /s /t 1")
  time.sleep(2)
