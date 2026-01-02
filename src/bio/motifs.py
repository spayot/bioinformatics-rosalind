from math import prod
import numpy as np
from bio.strings import (
    NUC2INT,
    find_all_approx_occurences,
    find_neighbors,
    hamming_distance,
    number_to_pattern,
)


def motif_enumeration(Dna: list[str], k: int, d: int) -> set[str]:
    patterns = set()
    for i in range(len(Dna[0]) - k + 1):
        pattern = Dna[0][i : i + k]
        for neighbor in find_neighbors(pattern, d):
            if all(find_all_approx_occurences(neighbor, dna, d) for dna in Dna[1:]):
                patterns.add(neighbor)
    return patterns


def distance(dna: str, pattern: str) -> tuple[int, str]:
    min_distance = 1e9
    best_match = ""
    k = len(pattern)
    for i in range(len(dna) - k + 1):
        kmer = dna[i : i + k]
        d = hamming_distance(kmer, pattern)
        if d < min_distance:
            min_distance = d
            best_match = kmer
    return int(min_distance), best_match


def total_distance(Dna: list[str], pattern: str) -> int:
    total = 0
    for dna in Dna:
        total += distance(dna, pattern)[0]
    return total


def median_string(Dna: list[str], k: int) -> str:
    min_d = 1e9
    median = ""
    for idx in range(4**k):
        pattern = number_to_pattern(idx, k)
        td = total_distance(Dna, pattern)

        if td < min_d:
            min_d = td
            median = pattern
    return median


def profile_based_probability(kmer: str, profile: np.ndarray) -> float:
    return prod(profile[NUC2INT[c], i] for i, c in enumerate(kmer))


def most_probable_kmer_from_profile(text: str, k: int, profile: np.ndarray) -> str:
    max_proba = 0
    most_probable_kmer = ""
    for i in range(len(text) - k + 1):
        kmer = text[i : i + k]
        kmer_proba = profile_based_probability(kmer, profile)
        if kmer_proba > max_proba:
            most_probable_kmer = kmer
            max_proba = kmer_proba
    return most_probable_kmer
