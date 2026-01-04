import sys

from bio.strings import reverse_complement
from bio.utils import read_inputs


def main() -> None:
    schema = [("pattern", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    print(reverse_complement(**args))


if __name__ == "__main__":
    main()
