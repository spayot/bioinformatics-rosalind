from bio.motifs import median_string, total_distance
from bio.utils import read_inputs


def main() -> None:
    """find median string of length k over a list of DNA sequences"""
    schema = [("k", int), ("Dna", str)]
    args = read_inputs(schema, last_as_a_list=True)

    # run algorithm
    print(median_string(**args))


#    print(total_distance(args["Dna"], "ACG"))


if __name__ == "__main__":
    main()
