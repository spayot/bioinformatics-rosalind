import sys
from bio.newspaper import composition
from bio.utils import print_output, read_inputs


def main() -> None:
    schema = [("k", int), ("text", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    output = composition(**args)
    # run algorithm
    print_output(output)


if __name__ == "__main__":
    main()
