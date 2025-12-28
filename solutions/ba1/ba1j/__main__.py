from bio.utils import read_inputs
from bio.strings import most_frequent_approx_kmers

schema = [("text", str), ("k", int), ("d", int)]


def main() -> None:
    args = read_inputs(schema)

    # run algorithm
    print(*most_frequent_approx_kmers(incl_reverse=True, **args))


if __name__ == "__main__":
    main()
