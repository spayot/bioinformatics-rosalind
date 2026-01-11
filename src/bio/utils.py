from pathlib import Path
from typing import Any


def read_inputs(
    filepath: Path | str, schema: list[tuple[str, type]], last_as_a_list: bool = False
) -> dict[str, Any]:
    """reads the arguments entered in a filepath provided through CLI (sys.argv[1]) and split them into a list of strings.
    Optionally, if a `schema` is provided, it converts argument to expected type

    """
    with open(filepath) as f:
        args: list[str] = f.read().strip().split()
    converted_values = {}
    for idx, ((field_name, field_type), value) in enumerate(zip(schema, args)):
        converted_values[field_name] = field_type(value)

    if last_as_a_list:
        converted_values[field_name] = [field_type(v) for v in args[idx:]]

    return converted_values


def print_output(output: Any) -> None:
    """default prints using \n separator for lists or sets"""
    if isinstance(output, list) | isinstance(output, set):
        print(*output, sep="\n")

    else:
        print(output)
