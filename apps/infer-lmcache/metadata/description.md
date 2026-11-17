# Infer: vLLM + LMCache

LMCache's vLLM image. Same vLLM flags as infer-vllm, but KV offload goes through LMCache's multi-process connector (LMCacheMPConnector, auto-started server) with a host-RAM L1 tier of KV_CPU_GB. LMCache 0.5.7 has Mamba/linear-attention snapshot support (kv_cache_groups.py); verify hits with the real hybrid model in the log.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
