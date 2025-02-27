import pyaudio
import numpy as np


class AudioStream:
    def __init__(self):
        self.CHUNK = 1600  # 40ms的音频块
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.p = pyaudio.PyAudio()

    def get_stream(self):
        return self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=self._find_microphone()
        )

    def _find_microphone(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0 and '麦克风' in dev['name']:
                return i
        return 0