import sys
from bio.motifs import greedy_motif_search
from bio.utils import read_inputs


def main() -> None:
    """greedy motif search with pseudocounts (adjusting the profile probability matrix by adding 1 to each count)"""
    schema = [("k", int), ("t", int), ("Dna", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=True)

    # run algorithm
    # print(*greedy_motif_search(with_pseudocounts=True, **args))
    print(*greedy_motif_search(with_pseudocounts=True, **args))


if __name__ == "__main__":
    main()
