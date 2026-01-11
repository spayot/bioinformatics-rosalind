import os
import sys

from bio.strings import most_frequent_kmers
from bio.utils import read_inputs


def main() -> None:
    schema = [("text", str), ("k", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    print(" ".join(most_frequent_kmers(**args)))


if __name__ == "__main__":
    main()
