# Infer: mistral.rs

mistral.rs 0.9.5 (CUDA 13.2, native sm_120 build), pinned by digest. A single Rust binary: loads the block-FP8 safetensors directly, PagedAttention with an FP8 KV cache, prefix caching, native MTP speculative decoding from the checkpoint head, Prometheus /metrics, and OpenAI plus Anthropic /v1/messages APIs. mistral.rs has no served-name flag, so the model directory is mounted at /models/<Served model name> and loaded by that relative name, which becomes the model id. Limits: no host-RAM KV tier (KV_CPU_GB is ignored), no request priority, and MAX_LEN is ignored (its loaders reject --max-model-len; the model's own context length applies). GPU_FRAC is a share of total VRAM minus other processes' use; set it to `none` and pass `--kv-cache 2GiB` in EXTRA_ARGS for a smoke test next to another engine.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
