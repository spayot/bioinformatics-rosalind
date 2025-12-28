from bio.utils import read_inputs

schema = [("text", str), ("k", int), ("d", int)]


def main() -> None:
    args = read_inputs(schema)

    # run algorithm
    print(args)


if __name__ == "__main__":
    main()
