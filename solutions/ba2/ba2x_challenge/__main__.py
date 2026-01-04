from bio.motifs import run_multiple_times, randomized_motif_search
from bio.utils import read_inputs


def main() -> None:
    """randomized motif search"""
    schema = [("Dna", str)]
    args = read_inputs(schema, True)
    # print(args)
    # run algorithm
    best_motifs = run_multiple_times(
        algorithm=randomized_motif_search, n=1000, k=20, t=10, **args
    )

    print(
        f"consensus: {best_motifs.consensus()}\nscore:     {best_motifs.score}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
