from dataclasses import dataclass
from typing import Annotated
from itertools import combinations, product


class Kmer(str):
    @property
    def k(self) -> int:
        return len(self)

    @property
    def suffix(self) -> str:
        return self[1:]

    @property
    def prefix(self) -> str:
        return self[:-1]


def composition(k: int, text: str) -> list[Kmer]:
    return sorted([Kmer(text[i : i + k]) for i in range(len(text) - k + 1)])


def genome_path_to_string(genome_path: list[Kmer]) -> str:
    return genome_path[0][:-1] + "".join([gp[-1] for gp in genome_path])


def overlap_graph(patterns: list[Kmer]) -> list[tuple[Kmer, Kmer]]:
    patterns.sort()
    return [
        (p1, p2) for p1, p2 in product(patterns, patterns) if p1.suffix == p2.prefix
    ]
