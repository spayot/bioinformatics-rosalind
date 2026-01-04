import sys
from bio.strings import find_clumps
from bio.utils import read_inputs


def main() -> None:
    schema = [("genome", str), ("k", int), ("L", int), ("t", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    print(*find_clumps(**args))


if __name__ == "__main__":
    main()
