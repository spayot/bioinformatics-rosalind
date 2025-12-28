from collections import defaultdict

import numpy as np


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


COMPLEMENTS = {"A": "T", "T": "A", "C": "G", "G": "C"}


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
