import sys
from bio.utils import read_inputs


def main() -> None:
    schema = [("pattern", str), ("text", str), ("d", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    # run algorithm
    print(args)


if __name__ == "__main__":
    main()
