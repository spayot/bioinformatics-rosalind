from bio.motifs import run_multiple_randomized_motif_search, greedy_motif_search
from bio.utils import read_inputs


def main() -> None:
    """randomized motif search"""
    schema = [("k", int), ("t", int), ("Dna", str)]
    args = read_inputs(schema, True)

    # print(args)
    # run algorithm
    best_motifs = run_multiple_randomized_motif_search(n=1000, **args)

    print(*best_motifs.kmers, sep="\n")


if __name__ == "__main__":
    main()
