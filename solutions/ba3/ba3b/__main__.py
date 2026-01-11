import sys
from bio.newspaper import genome_path_to_string
from bio.utils import read_inputs, print_output


def main() -> None:
    schema = [("genome_path", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=True)

    # run algorithm
    print_output(genome_path_to_string(**args))


if __name__ == "__main__":
    main()
