# system_integration.py 新增光标检测功能
import ctypes
import ctypes.wintypes
import pyautogui
import time
# 定义Windows API需要的结构和函数
user32 = ctypes.windll.user32

class SystemInterface:
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    user32.GetCaretPos.restype = ctypes.wintypes.BOOL
    user32.GetCaretPos.argtypes = [ctypes.POINTER(POINT)]

    @staticmethod
    def has_caret():
        """检测系统当前是否存在文本输入光标"""
        caret_pos = SystemInterface.POINT()
        return user32.GetCaretPos(ctypes.byref(caret_pos))

    @staticmethod
    def input_text(text):
        """在光标位置输入文本（带安全检测）"""
        if SystemInterface.has_caret():
            print(f"检测到输入光标，正在输入文本:{text}")
            pyautogui.write(text)
            time.sleep(1)  # 输入间隔防止冲突
            return True
        return False

    @staticmethod
    def show_alert(message):
        """显示系统通知（实现需根据平台调整）"""
        # 此处可替换为实际的系统通知实现
        print(f"系统提示：{message}")

    @staticmethod
    def has_focus():
        """窗口焦点检测（可选保留原有逻辑）"""
        return True  # 可根据需要实现具体逻辑