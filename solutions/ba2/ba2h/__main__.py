"""
Rosalind ID: ba2h
Title: Implement DistanceBetweenPatternAndStrings
URL: https://rosalind.info/problems/ba2h/
"""

import sys
from bio.motifs import total_distance
from bio.utils import read_inputs


def main() -> None:
    """Implement DistanceBetweenPatternAndStrings"""
    schema = [("pattern", str), ("Dna", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=True)

    # run algorithm
    print(total_distance(**args))


if __name__ == "__main__":
    main()
