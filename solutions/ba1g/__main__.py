from bio.strings import hamming_distance
from bio.utils import read_inputs
from typing import Any


def parse_string(s: str) -> Any:
    return s


def main() -> None:
    args = read_inputs()

    # parse inputs
    s1, s2 = args

    # run algorithm
    print(f"{len(s1)=}")
    print(f"{hamming_distance(s1, s2)=}")


if __name__ == "__main__":
    main()
