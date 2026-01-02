from collections import defaultdict
from itertools import combinations, product
from typing import Iterable, Literal

import numpy as np

NucleicAcids = Literal["A", "C", "G", "T"]
COMPLEMENTS = {"A": "T", "T": "A", "C": "G", "G": "C"}

NUC2INT = {"A": 0, "C": 1, "G": 2, "T": 3}
INT2NUC = {v: k for k, v in NUC2INT.items()}


def most_frequent_kmers(text: str, k: int) -> list[str]:
    kmers = defaultdict(int)

    for i in range(len(text) - k + 1):
        kmers[text[i : i + k]] += 1

    mfkm = []
    max_freq = 0
    for kmer, freq in kmers.items():
        if freq < max_freq:
            continue
        elif freq > max_freq:
            mfkm = [kmer]
            max_freq = freq
        else:
            mfkm.append(kmer)

    return mfkm


def reverse_complement(pattern: str) -> str:
    return "".join([COMPLEMENTS[c] for c in pattern[::-1]])


def find_all_occurences(pattern: str, text: str) -> list[int]:
    k = len(pattern)
    occurences = []
    for i in range(len(text) - k + 1):
        if text[i : i + k] == pattern:
            occurences.append(i)

    return occurences


def find_clumps(genome: str, k: int, L: int, t: int) -> set[str]:
    clumps = set()
    kmers_freq = defaultdict(int)
    for i in range(len(genome) - k + 1):
        if i >= L:
            kmers_freq[genome[i - L : i - L + k]] -= 1

        kmer = genome[i : i + k]
        kmers_freq[kmer] += 1

        if (kmer not in clumps) & (kmers_freq[kmer] >= t):
            clumps.add(kmer)

    return clumps


def skew(genome: str) -> np.ndarray:
    skews = [0]
    skew = 0
    for c in genome:
        match c:
            case "G":
                skew += 1
            case "C":
                skew -= 1
            case _:
                pass

        skews.append(skew)

    return np.array(skews)


def argmins(ar: np.ndarray) -> list[int]:
    """returns all indices of a 1d-array which value are equal to the array's minimum"""
    minimum = ar.min()
    return [idx for idx, val in enumerate(ar) if val == minimum]


def hamming_distance(s1: str, s2: str) -> int:
    assert len(s1) == len(s2), "hamming distance expects two sequences of same length"
    return sum([1 for c1, c2 in zip(s1, s2) if c1 != c2])


def find_all_approx_occurences(pattern: str, text: str, d: int = 0) -> list[int]:
    k = len(pattern)
    occurences = []
    for i in range(len(text) - k + 1):
        if hamming_distance(text[i : i + k], pattern) <= d:
            occurences.append(i)

    return occurences


def build_mismatched_kmer(
    kmer: str, idx: Iterable[int], mismatches: Iterable[str]
) -> str:
    neighbor = list(kmer)
    for i, m in zip(idx, mismatches):
        neighbor[i] = m
    return "".join(neighbor)


def find_neighbors(pattern: str, d: int) -> set[str]:
    k = len(pattern)
    neighbors = set()
    for idx in combinations(range(k), d):
        for mismatches in product(*["ACTG" for _ in range(d)]):
            neighbors.add(build_mismatched_kmer(pattern, idx, mismatches))

    return neighbors


def approx_kmers_frequency(text: str, k: int, d: int) -> dict[str, int]:
    neighbor_freq = defaultdict(int)
    for i in range(len(text) - k + 1):
        for neighbor in find_neighbors(text[i : i + k], d):
            neighbor_freq[neighbor] += 1

    return neighbor_freq


def most_frequent_approx_kmers(
    text: str, k: int, d: int, incl_reverse: bool = False
) -> set[str]:
    neighbor_freq = approx_kmers_frequency(text, k, d)

    if incl_reverse:
        nf2 = {}
        for kmer in neighbor_freq:
            rc = reverse_complement(kmer)
            nf2[kmer] = neighbor_freq[kmer]
            if rc in neighbor_freq:
                nf2[kmer] += neighbor_freq[rc]

        neighbor_freq = nf2

    max_freq = max(neighbor_freq.values())
    return set(kmer for kmer, freq in neighbor_freq.items() if freq == max_freq)


def pattern_to_number(pattern: str) -> int:
    """ba1k"""
    return sum(4**i * NUC2INT[c] for i, c in enumerate(list(pattern)[::-1]))


def computing_frequencies(text: str, k: int) -> np.ndarray:
    """ba1k"""
    freqs = np.zeros((4**k), dtype=np.int64)

    for i in range(len(text) - k + 1):
        freqs[pattern_to_number(text[i : i + k])] += 1

    return freqs


def number_to_pattern(idx: int, k: int) -> str:
    n = idx
    pattern = []
    for i in range(k):
        pattern.append(INT2NUC[n % 4])
        n = n // 4

    return "".join(pattern[::-1])


def neighbors_v2(pattern: str, d: int) -> set[str]:
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {"A", "C", "G", "T"}
    neighborhood = set()

    suffix_neighbors = neighbors_v2(pattern[1:], d)
    for sn in suffix_neighbors:
        if hamming_distance(pattern[1:], sn) < d:
            for n in "ACGT":
                neighborhood.add(n + sn)
        else:
            neighborhood.add(pattern[0] + sn)

    return neighborhood


def motif_enumeration(Dna: list[str], k: int, d: int) -> set[str]:
    patterns = set()
    for i in range(len(Dna[0]) - k + 1):
        pattern = Dna[0][i : i + k]
        for neighbor in find_neighbors(pattern, d):
            if all(find_all_approx_occurences(neighbor, dna, d) for dna in Dna[1:]):
                patterns.add(neighbor)
    return patterns
