import sys
from bio.motifs import most_probable_kmer_from_profile
from bio.utils import read_inputs
import numpy as np


def main() -> None:
    """find kmer with highest probability within a string given a profile"""
    schema = [("text", str), ("k", int), ("profile", float)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=True)

    args["profile"] = np.array(args["profile"]).reshape(4, -1)

    # run algorithm
    print(most_probable_kmer_from_profile(**args))


if __name__ == "__main__":
    main()
