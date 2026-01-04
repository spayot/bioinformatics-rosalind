import sys
from bio.motifs import GibbsSampler, run_multiple_times
from bio.utils import read_inputs


def main() -> None:
    """randomized motif search"""
    schema = [("k", int), ("t", int), ("N", int), ("Dna", str)]
    args = read_inputs(sys.argv[1], schema, True)

    # run algorithm
    best_motifs = run_multiple_times(algorithm=GibbsSampler, n=20, **args)

    print(*best_motifs.kmers, sep="\n")


if __name__ == "__main__":
    main()
