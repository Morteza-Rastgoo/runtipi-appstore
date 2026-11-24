# Infer: llama.cpp server

llama.cpp llama-server build 12679 (CUDA 13, native sm_120 kernels), pinned by digest. Serves a GGUF conversion of the model (Q8_0) with its vision projector, flash attention, q8_0 KV in one unified buffer shared by all slots, context checkpoints for the hybrid (Gated DeltaNet) layers, a host-RAM prompt cache (--cache-ram), native MTP speculative decoding (--spec-type draft-mtp, from the NextN tensors kept in the GGUF), Prometheus /metrics, /slots, and OpenAI plus Anthropic /v1/messages APIs. Limits: no request priority, and GPU_FRAC is ignored (VRAM use follows the KV pool size).

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
