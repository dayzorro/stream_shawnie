from faster_whisper import WhisperModel
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

model_size = "base"

# Run on GPU with FP16
# model = WhisperModel(
#     "./models2/Systran/faster-whisper-medium",  # Direct path
#     device="cuda",
#     compute_type="float16"
# )

model = WhisperModel(
        "base",
        device="cuda",
        compute_type="int8",
        download_root="../models",
        local_files_only=True
        )
# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("../audio/audio.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
