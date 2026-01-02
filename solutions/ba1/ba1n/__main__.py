from bio.strings import find_neighbors, neighbors_v2, hamming_distance
from bio.utils import read_inputs


def main() -> None:
    schema = [("pattern", str), ("d", int)]
    args = read_inputs(schema)

    # run algorithm
    # print(*neighbors_v2(**args))

    # s = find_neighbors(**args)
    # print({c: hamming_distance(args["kmer"], c) for c in s})

    s1 = neighbors_v2(**args)
    s2 = find_neighbors(**args)

    diff = s1.symmetric_difference(s2)
    if not diff:
        print("both methods return the same output.")
    else:
        print("different output")
        print(diff)


if __name__ == "__main__":
    main()
