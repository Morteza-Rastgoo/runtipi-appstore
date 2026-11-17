# Infer: SGLang

SGLang v0.5.23 (CUDA 13). Radix prefix cache with Mamba-state tracking for Qwen3.5 hybrid models, HiCache host-RAM KV tier (KV_CPU_GB), NEXTN/MTP speculative decoding, priority scheduling, Prometheus /metrics, OpenAI and Anthropic /v1/messages APIs. Note: --mem-fraction-static is a share of TOTAL VRAM that SGLang may use, and it requires (1 - fraction) x total to be free after loading weights; while the host vLLM is running use 0.95 with the MPS cap (0=12G) as the real limit. Claude Code clients should set CLAUDE_CODE_ATTRIBUTION_HEADER=0 so the system prompt prefix stays cacheable.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
