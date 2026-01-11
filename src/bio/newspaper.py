def composition(k: int, text: str) -> list[str]:
    return sorted([text[i : i + k] for i in range(len(text) - k + 1)])


def genome_path_to_string(genome_path: list[str]) -> str:
    return genome_path[0][:-1] + "".join([gp[-1] for gp in genome_path])
