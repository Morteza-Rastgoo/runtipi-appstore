# Infer: NVIDIA Dynamo (vLLM backend)

NVIDIA Dynamo 1.6.2 single-node aggregated serving: dynamo.frontend (Rust OpenAI/Anthropic HTTP server, tool and reasoning parsing) plus one dynamo.vllm worker (bundled vLLM 0.31.0, registers Qwen3_5ForConditionalGeneration). Discovery uses the local file backend, so no etcd or NATS is needed. Prefix caching, chunked prefill, fp8 KV, native MTP and CPU KV offload are vLLM engine flags. Frontend metrics: /metrics on the API port. Worker (vLLM) metrics: DYN_SYSTEM_PORT 8081 inside the container. The KV-aware router matters only with 2+ workers; this app runs one.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
