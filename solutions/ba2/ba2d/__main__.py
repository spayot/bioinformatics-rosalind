from bio.motifs import greedy_motif_search
from bio.utils import read_inputs


def main() -> None:
    schema = [("k", int), ("t", int), ("Dna", str)]
    args = read_inputs(schema, True)

    # run algorithm
    print(*greedy_motif_search(**args))


if __name__ == "__main__":
    main()
