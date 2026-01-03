from copy import deepcopy
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
    most_probable_kmer = text[:k]
    for i in range(len(text) - k + 1):
        kmer = text[i : i + k]
        kmer_proba = profile_based_probability(kmer, profile)
        if kmer_proba > max_proba:
            most_probable_kmer = kmer
            max_proba = kmer_proba
    return most_probable_kmer


def build_profile(motifs: list[str], with_pseudocounts: bool = False) -> np.ndarray:
    """creates a frequency-based probability matrix to find each nucleotide (rows) for each position of the k-mer (columns)"""
    k = len(motifs[0])
    t = len(motifs)
    profile = np.zeros((4, k))
    for motif in motifs:
        for i, c in enumerate(motif):
            profile[NUC2INT[c], i] += 1
    if with_pseudocounts:
        # adding 1 count to each nucleic acid to avoid zero probabilities
        profile += 1
        t += 4
    return profile / t


def score(motifs: list[str], with_pseudocounts: bool = False) -> int:
    """scores motifs distance to consensus string"""
    distance_to_consensus = 1 - build_profile(motifs, with_pseudocounts).max(axis=0)
    return int(distance_to_consensus.sum() * len(motifs))


def greedy_motif_search(
    Dna: list[str], k: int, t: int, with_pseudocounts: bool = False
) -> list[str]:
    best_motifs = [dna[:k] for dna in Dna]
    for i in range(len(Dna[0]) - k + 1):
        motif1 = Dna[0][i : i + k]
        motifs = [motif1]
        for j in range(1, t):
            profile = build_profile(motifs, with_pseudocounts)
            motifs.append(most_probable_kmer_from_profile(Dna[j], k, profile))

        if score(motifs) < score(best_motifs):
            best_motifs = deepcopy(motifs)
    return best_motifs
