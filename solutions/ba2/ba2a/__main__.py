from bio.utils import read_inputs
from bio.motifs import motif_enumeration


def main() -> None:
    schema = [("k", int), ("d", int), ("Dna", str)]
    args = read_inputs(schema, last_as_a_list=True)

    # run algorithm
    print(*motif_enumeration(**args))


if __name__ == "__main__":
    main()
