from audio_stream import AudioStream
from whisper_stream import WhisperTranscriber
from faster_whisper import WhisperModel
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
        self.last_voice = time.time()  # 正确初始化位置

    def run(self):
        stream = self.audio_stream.get_stream()
        print("开始监听...")

        while True:
            data = stream.read(self.audio_stream.CHUNK)
            audio_np = np.frombuffer(data, dtype=np.int16)
            # print(audio_np)
            # 实时转写
            text = self.transcriber.transcribe_stream(audio_np)
            if len(text)>0:
                print(text)

            if not self.is_active:
                # print(self.wake_detector.check_wake_word(text))
                if self.wake_detector.check_wake_word(text):
                    self.is_active = True
                    SystemInterface.show_alert(" 已唤醒，请开始说话")
            else:
                if len(text) > 0:
                    print("OK->"+text)
                    self.last_voice = time.time()  # 每次检测到语音时更新
                    if SystemInterface.has_focus():
                        SystemInterface.input_text(text)
                    else:
                        SystemInterface.show_alert(" 未检测到光标！")

                # 静音3秒后休眠
                if time.time() - self.last_voice > 15:
                    self.is_active = False


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()