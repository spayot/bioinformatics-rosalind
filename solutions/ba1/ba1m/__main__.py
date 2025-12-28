from bio.strings import number_to_pattern
from bio.utils import read_inputs


def main() -> None:
    schema = [("idx", int), ("k", int)]
    args = read_inputs(schema)

    # run algorithm
    print(number_to_pattern(**args))


if __name__ == "__main__":
    main()
