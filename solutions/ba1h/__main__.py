import sys
from bio.strings import find_all_approx_occurences
from bio.utils import read_inputs


def main() -> None:
    # parse inputs
    args = read_inputs(schema=[("pattern", str), ("text", str), ("d", int)])

    # run algorithm
    print(*find_all_approx_occurences(**args))


if __name__ == "__main__":
    main()
