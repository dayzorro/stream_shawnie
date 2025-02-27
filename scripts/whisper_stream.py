from faster_whisper import WhisperModel
import numpy as np
# from faster_whisper import WhisperModel
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# model_size = "medium"
model_size = "./models/whisper-tiny-zh-ct2"


class WhisperTranscriber:
    def __init__(self):
        self.model = WhisperModel(
            model_size,
            device="cuda",
            compute_type="float16",
            download_root="../models",
            local_files_only=True
        )
        self.buffer = np.array([], dtype=np.float32)

    def transcribe_stream(self, audio_chunk):
        # 将int16转为float32
        audio_f32 = audio_chunk.astype(np.float32) / 32768.0
        self.buffer = np.concatenate([self.buffer, audio_f32])

        # 每2秒处理一次
        if len(self.buffer) < 32000 * 2:
            return ""

        segments, _ = self.model.transcribe(
            self.buffer,
            language="zh",
            beam_size=5,
            vad_filter=True
        )

        result = "".join([seg.text for seg in segments])
        self.buffer = self.buffer[-16000:]  # 保留最后1秒作为上下文
        return result