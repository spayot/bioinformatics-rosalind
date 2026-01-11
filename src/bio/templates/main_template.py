import sys
from bio.utils import read_inputs, print_output


def main() -> None:
    schema = [("k", int), ("patterns", list[str])]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    # run algorithm
    print_output(args)


if __name__ == "__main__":
    main()
