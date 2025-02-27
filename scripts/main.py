# voice_assistant.py 修改后的主程序
from audio_stream import AudioStream
from whisper_stream import WhisperTranscriber
from wake_detector import WakeWordDetector
from system_integration import SystemInterface
import time
import numpy as np
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


class VoiceAssistant:
    def __init__(self):
        self.audio_stream = AudioStream()
        self.transcriber = WhisperTranscriber()
        self.wake_detector = WakeWordDetector()
        self.is_active = False
        self.last_voice = time.time()
        self.input_cooldown = 0  # 输入冷却计时器

    def run(self):
        stream = self.audio_stream.get_stream()
        print("语音助手已启动，等待唤醒词...")

        while True:
            # 冷却期处理
            if self.input_cooldown > 0:
                self.input_cooldown -= self.audio_stream.CHUNK / 1000
                time.sleep(self.audio_stream.CHUNK / 1000)
                continue

            data = stream.read(self.audio_stream.CHUNK)
            audio_np = np.frombuffer(data, dtype=np.int16)

            # 语音转写
            text = self.transcriber.transcribe_stream(audio_np)
            if len(text) > 0:
                print(f"原始转写：{text}")

            # 状态机控制
            if not self.is_active:
                if self.wake_detector.check_wake_word(text):
                    self.activate_assistant()
            else:
                self.process_voice_input(text)

    def activate_assistant(self):
        self.is_active = True
        self.last_voice = time.time()
        SystemInterface.show_alert("已唤醒，请开始说话")
        print("--> 语音输入模式激活 <--")

    def process_voice_input(self, text):
        if len(text) > 0:
            print(f"语音输入：{text}")
            self.last_voice = time.time()

            if SystemInterface.input_text(text):
                self.input_cooldown = 0.5  # 成功输入后设置冷却
            else:
                SystemInterface.show_alert("输入失败：未检测到光标")
                self.input_cooldown = 1

        # 15秒无语音自动休眠
        if time.time() - self.last_voice > 15:
            self.is_active = False
            SystemInterface.show_alert("语音助手已休眠")
            print("--> 返回休眠状态 <--")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()