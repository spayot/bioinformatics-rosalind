import sys
from bio.strings import hamming_distance
from bio.utils import read_inputs
from typing import Any


def parse_string(s: str) -> Any:
    return s


def main() -> None:
    schema = [("s1", str), ("s2", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    print(hamming_distance(**args))


if __name__ == "__main__":
    main()
