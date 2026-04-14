import os
from huggingface_hub import snapshot_download

def download_explanation_model():
    model_id = "Qwen/Qwen2.5-3B-Instruct"
    # Point exactly to your local gitignored folder
    local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "explanation"))
    
    print(f"Downloading {model_id} directly to {local_dir}...")
    
    # snapshot_download pulls the repo directly into the folder you specify
    # local_dir_use_symlinks=False prevents the weird Windows symlink warning you saw
    snapshot_download(
        repo_id=model_id, 
        local_dir=local_dir,
        local_dir_use_symlinks=False,
        ignore_patterns=["*.msgpack", "*.h5", "coreml/*"] # Skip weights we don't need
    )
    print("Download complete! Models are now stored locally.")

if __name__ == "__main__":
    download_explanation_model()