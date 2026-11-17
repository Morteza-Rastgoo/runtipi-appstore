# Infer: Xinference (vLLM engine)

Xinference v4.2.0 slim image: a supervisor + worker with a web UI on the API port, an OpenAI and Anthropic API, and a model registry. The image ships no engine: on the first launch Xinference pip-installs vLLM into a per-model virtualenv under /data/xinference (needs internet, several GB, several minutes). The `qwen3.8` family pins vllm==0.21.0; Qwen3-Instruct takes the newest vLLM. The app starts the server, then launches MODEL as uid SERVED_NAME. Prefix caching and fp8 KV are passed as vLLM kwargs. SPEC_TOKENS, KV_CPU_GB and CHAT_TEMPLATE are ignored (Xinference uses the family template). Worker metrics: port 9998 inside the container.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
