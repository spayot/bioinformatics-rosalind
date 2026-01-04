import sys
from bio.strings import pattern_to_number
from bio.utils import read_inputs

schema = [("pattern", str)]


def main() -> None:
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    # run algorithm
    print(pattern_to_number(**args))


if __name__ == "__main__":
    main()
