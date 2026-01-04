import sys
from bio.utils import read_inputs
from bio.strings import most_frequent_approx_kmers


def main() -> None:
    schema = [("text", str), ("k", int), ("d", int)]
    args = read_inputs(filepath=sys.argv[1], schema=schema, last_as_a_list=False)

    # run algorithm

    # print(len(find_neighbors("GTAGG", 2)))
    print(*most_frequent_approx_kmers(**args))


if __name__ == "__main__":
    main()
