# Infer: LMDeploy (PyTorch engine)

LMDeploy v0.18.0 PyTorch backend (Qwen3.5 hybrid models are not on TurboMind). Prefix caching, fp8 KV (quant-policy fp8), Triton FP8 GEMM and Triton attention (DeepGEMM and FA3 have no sm_120 kernels, so they are disabled; qwen3_5_mtp speculative decoding requires FA3 and is therefore off: SPEC_TOKENS is ignored). Prometheus /metrics, OpenAI and Anthropic APIs. GPU_FRAC maps to --cache-max-entry-count, which is the share of FREE memory after weights used for KV (not of total VRAM). KV_CPU_GB is ignored: LMDeploy has no host-RAM KV tier. CHAT_TEMPLATE is ignored: LMDeploy's --chat-template takes its own JSON format, so the model's bundled Jinja template is used.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
