from collections import deque


class WakeWordDetector:
    def __init__(self, wake_word="语音"):
        self.wake_word = wake_word
        self.history = deque(maxlen=5)  # 保存最近5次识别结果

    def check_wake_word(self, text):
        self.history.append(text)
        combined = "".join(self.history)
        return self.wake_word in combined