import pyautogui
import tkinter as tk
from pynput import keyboard


class SystemInterface:
    @staticmethod
    def input_text(text):
        try:
            pyautogui.write(text, interval=0.02)
        except pyautogui.FailSafeException:
            SystemInterface.show_alert(" 未找到光标位置！")

    @staticmethod
    def show_alert(message):
        root = tk.Tk()
        root.overrideredirect(1)
        root.geometry("300x60+{}+{}".format(
            root.winfo_screenwidth() - 320,
            root.winfo_screenheight() - 100))

        label = tk.Label(root, text=message, font=('微软雅黑', 12))
        label.pack(pady=15)
        root.after(3000, root.destroy)
        root.mainloop()

    @staticmethod
    def has_focus():
        # 使用Windows API检测光标状态
        import win32gui
        foreground = win32gui.GetForegroundWindow()
        return foreground != 0