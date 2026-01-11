import sys
from bio.utils import read_inputs

from bio.strings import find_all_occurences


def main() -> None:
    schema = [("pattern", str), ("text", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    print(*(str(i) for i in find_all_occurences(**args)))


if __name__ == "__main__":
    main()
