from bio.utils import read_inputs


def main() -> None:
    schema = [("k", int), ("t", int), ("Dna", str)]
    args = read_inputs(schema, True)

    # run algorithm
    print(args)


if __name__ == "__main__":
    main()
