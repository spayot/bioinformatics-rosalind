import sys
from bio.motifs import run_multiple_times, randomized_motif_search
from bio.utils import read_inputs


def main() -> None:
    """randomized motif search"""
    schema = [("k", int), ("t", int), ("Dna", list[str])]
    args = read_inputs(sys.argv[1], schema)

    # run algorithm
    best_motifs = run_multiple_times(algorithm=randomized_motif_search, n=1000, **args)

    print(*best_motifs.kmers, sep="\n")


if __name__ == "__main__":
    main()
