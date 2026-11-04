"""Optional local Ollama reviewer; suggestions only, never executed as trades."""


class OllamaReviewer:
    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        self.model, self.base_url = model, base_url.rstrip("/")

    def review(self, summary: str) -> str:
        try:
            import requests
        except ImportError as exc:
            raise RuntimeError("Install requests to use the optional Ollama reviewer") from exc
        response = requests.post(f"{self.base_url}/api/generate",
                                 json={"model": self.model, "prompt": summary, "stream": False},
                                 timeout=60)
        response.raise_for_status()
        return str(response.json().get("response", ""))
