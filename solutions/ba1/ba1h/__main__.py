import sys
from bio.strings import find_all_approx_occurences
from bio.utils import read_inputs


def main() -> None:
    # parse inputs
    schema = [("pattern", str), ("text", str), ("d", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema)
    # run algorithm
    print(*find_all_approx_occurences(**args))


if __name__ == "__main__":
    main()
