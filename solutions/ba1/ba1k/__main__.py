import sys
from bio.strings import computing_frequencies
from bio.utils import read_inputs

schema = [("text", str), ("k", int)]


def main() -> None:
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    # run algorithm
    print(*computing_frequencies(**args))


if __name__ == "__main__":
    main()
