def composition(k: int, text: str) -> list[str]:
    return sorted([text[i : i + k] for i in range(len(text) - k + 1)])
