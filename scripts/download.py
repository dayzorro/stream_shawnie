from huggingface_hub import snapshot_download

snapshot_download(repo_id="openai/whisper-medium", local_dir="../models")