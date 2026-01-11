import sys
from bio.utils import read_inputs
from bio.motifs import motif_enumeration


def main() -> None:
    schema = [("k", int), ("d", int), ("Dna", list[str])]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    # run algorithm
    print(*motif_enumeration(**args))


if __name__ == "__main__":
    main()
