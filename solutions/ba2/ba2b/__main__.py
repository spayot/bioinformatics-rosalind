import sys
from bio.motifs import median_string
from bio.utils import read_inputs


def main() -> None:
    """find median string of length k over a list of DNA sequences"""
    schema = [("k", int), ("Dna", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=True)

    # run algorithm
    print(median_string(**args))


if __name__ == "__main__":
    main()
