import os
import time
import ctypes
from ctypes import wintypes
from rich import print

# 文件路径
file_path = r"C:\Users\YanJun\Desktop\新建文件夹\材料.zip"

# 转换为 Windows 时间戳
def to_windows_time(timestamp):
    return int((timestamp + 11644473600) * 10000000)

# 时间戳
create_time = to_windows_time(time.mktime(time.strptime("2024-11-29 17:57:23", "%Y-%m-%d %H:%M:%S")))
modify_time = to_windows_time(time.mktime(time.strptime("2024-11-29 17:57:44", "%Y-%m-%d %H:%M:%S")))
# 打开文件句柄
kernel32 = ctypes.windll.kernel32
handle = kernel32.CreateFileW(
    file_path, 256, 0, None, 3, 0x80, None
)

if handle == -1:
    raise ctypes.WinError()

# 创建时间、访问时间、修改时间
ft_create = wintypes.FILETIME(create_time & 0xFFFFFFFF, create_time >> 32)
ft_access = wintypes.FILETIME(modify_time & 0xFFFFFFFF, modify_time >> 32)  # 设置访问时间和修改时间一致
ft_write = wintypes.FILETIME(modify_time & 0xFFFFFFFF, modify_time >> 32)  # 设置修改时间为与访问时间相同

# 设置文件时间
success = kernel32.SetFileTime(handle, ctypes.byref(ft_create), ctypes.byref(ft_access), ctypes.byref(ft_write))
kernel32.CloseHandle(handle)

if not success:
    raise ctypes.WinError()

print("File creation, access, and modification times updated.")
