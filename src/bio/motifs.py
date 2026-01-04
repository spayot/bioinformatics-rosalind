from copy import deepcopy
from dataclasses import dataclass
from math import prod
import random
from typing import Callable

import numpy as np

from bio.strings import (
    INT2NUC,
    NUC2INT,
    find_all_approx_occurences,
    find_neighbors,
    hamming_distance,
    number_to_pattern,
)


@dataclass
class Motifs:
    kmers: list[str]

    def __post_init__(self) -> None:
        self.kmers = [kmer.upper() for kmer in self.kmers]
        self.k = len(self.kmers[0])

    def __getitem__(self, idx: int) -> str:
        return self.kmers[idx]

    def __setitem__(self, idx: int, value: str) -> None:
        self.kmers[idx] = value

    def __iter__(self):
        return self.kmers.__iter__()

    def append(self, obj: str) -> None:
        self.kmers.append(obj.upper())

    def pop(self, idx: int) -> None:
        self.kmers.pop(idx)

    @property
    def t(self) -> int:
        return len(self.kmers)

    @property
    def counts(self) -> np.ndarray:
        cnts = np.zeros((4, self.k), dtype=np.uint8)
        for motif in self.kmers:
            for i, c in enumerate(motif):
                cnts[NUC2INT[c], i] += 1
        return cnts

    def consensus(self) -> str:
        return "".join([INT2NUC[x] for x in self.counts.argmax(axis=0)])

    @property
    def score(self) -> int:
        """scores motifs distance to consensus string"""
        return int((self.t - self.counts.max(axis=0)).sum())

    def profile(self, with_pseudocounts: bool = False) -> np.ndarray:
        """creates a frequency-based probability matrix to find each nucleotide (rows) for each position of the k-mer (columns)"""
        if not with_pseudocounts:
            return self.counts / self.t
        else:
            cnts = self.counts + 1
            return cnts / (self.t + 4)


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


def greedy_motif_search(
    Dna: list[str], k: int, t: int, with_pseudocounts: bool = False
) -> Motifs:
    # initialize with first kmer for each dna strand
    best_motifs = Motifs([dna[:k] for dna in Dna])

    for i in range(len(Dna[0]) - k + 1):
        motif1 = Dna[0][i : i + k]
        motifs = Motifs([motif1])
        for j in range(1, t):
            motifs.append(
                most_probable_kmer_from_profile(
                    Dna[j], k, motifs.profile(with_pseudocounts)
                )
            )
        if motifs.score < best_motifs.score:
            best_motifs = deepcopy(motifs)
    return best_motifs


def motifs_from_profile(profile: np.ndarray, Dna: list[str]) -> Motifs:
    """each motif selected from Dna strands maximizes likelihood given profile."""
    k = profile.shape[1]
    return Motifs([most_probable_kmer_from_profile(dna, k, profile) for dna in Dna])


def random_motif_initialization(k: int, t: int, Dna: list[str]) -> Motifs:
    # random initialization
    starting_indices = [random.randint(0, len(Dna[i]) - k) for i in range(t)]
    return Motifs([Dna[i][j : j + k] for i, j in enumerate(starting_indices)])


def randomized_motif_search(k: int, t: int, Dna: list[str]) -> Motifs:
    # random initialization
    motifs = random_motif_initialization(k, t, Dna)
    best_motifs = deepcopy(motifs)

    while True:
        motifs = motifs_from_profile(motifs.profile(with_pseudocounts=True), Dna)
        if motifs.score < best_motifs.score:
            best_motifs = deepcopy(motifs)
        else:
            return best_motifs


def run_multiple_times(algorithm: Callable, n: int = 1000, **args) -> Motifs:
    best_score = 1e9
    for _ in range(n):
        motifs = algorithm(**args)
        if motifs.score < best_score:
            best_motifs = deepcopy(motifs)
            best_score = motifs.score

    return best_motifs


def masked_counts(motifs: Motifs, idx: int) -> np.ndarray:
    # calculate profile of motifs if you exclude motif[idx]
    assert idx < motifs.t, f"{idx=} should be lower than {motifs.t}"
    masked_count = (motifs.counts - Motifs([motifs[idx]]).counts) + 1
    return masked_count.astype(np.uint64)


def sample_motif_from_masked_counts(dna: str, k: int, masked_count: np.ndarray) -> int:
    # build proba distribution across kmers of Dna

    kmer_candidates = np.arange(len(dna) - k + 1)
    weights = np.array(
        [
            int(profile_based_probability(dna[c : c + k], masked_count))
            for c in kmer_candidates
        ]
    )
    weights = weights / weights.sum()  # normalize

    rng = np.random.default_rng()
    return int(rng.choice(kmer_candidates, p=weights, size=1)[0])


def GibbsSampler(k: int, t: int, N: int, Dna: list[str]) -> Motifs:
    motifs = random_motif_initialization(k, t, Dna)
    best_motifs = deepcopy(motifs)
    for _ in range(N):
        idx = random.choice(range(t))
        masked_count = masked_counts(motifs, idx)
        motif_start = sample_motif_from_masked_counts(Dna[idx], k, masked_count)
        motifs[idx] = Dna[idx][motif_start : motif_start + k]
        if motifs.score < best_motifs.score:
            best_motifs = deepcopy(motifs)

    return motifs
