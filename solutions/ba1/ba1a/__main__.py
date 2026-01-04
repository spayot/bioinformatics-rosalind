import sys

from bio.strings import pattern_count
from bio.utils import read_inputs


def main() -> None:
    schema = [("text", str), ("pattern", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    print(pattern_count(**args))


if __name__ == "__main__":
    main()
