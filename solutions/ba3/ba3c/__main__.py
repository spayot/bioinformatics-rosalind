import sys
from bio.core import Kmer
from bio.newspaper import overlap_graph
from bio.utils import read_inputs, print_output


def main() -> None:
    schema = [("patterns", list[Kmer])]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    # run algorithm
    og = overlap_graph(**args)

    output = [f"{p1} -> {p2}" for (p1, p2) in og]
    print_output(output)


if __name__ == "__main__":
    main()
