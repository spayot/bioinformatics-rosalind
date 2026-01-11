import sys
from bio.utils import read_inputs, print_output


def main() -> None:
    schema = [("pattern", str), ("text", str), ("d", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    # run algorithm
    print_output(args)


if __name__ == "__main__":
    main()
