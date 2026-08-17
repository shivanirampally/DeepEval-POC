from config.settings import (
    OLLAMA_QWEN_MODEL,
    OLLAMA_PHI3_MODEL,
    GEMINI_MODEL,
    DEEPSEEK_MODEL,
    OLLAMA_QWEN_URL,
    OLLAMA_PHI3_URL,
)

GENERATORS = [
    {
        "provider": "ollama",
        "display_name": "Ollama-Qwen3",
        "model": OLLAMA_QWEN_MODEL,
        "base_url": OLLAMA_QWEN_URL,
        "enabled": True,
    },
    {
        "provider": "ollama",
        "display_name": "Phi3",
        "model": OLLAMA_PHI3_MODEL,
        "base_url": OLLAMA_PHI3_URL,
        "enabled": True,
    },
    {
        "provider": "gemini",
        "display_name": "Gemini",
        "model": GEMINI_MODEL,
        "enabled": True,
    },
    {
        "provider": "deepseek",
        "display_name": "DeepSeek",
        "model": DEEPSEEK_MODEL,
        "enabled": True,
    },
]