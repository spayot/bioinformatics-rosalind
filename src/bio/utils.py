from pathlib import Path
from typing import Any, get_origin, get_args


def read_inputs(filepath: Path | str, schema: list[tuple[str, type]]) -> dict[str, Any]:
    """
    Reads file content and maps it to a schema.
    Supports single values and list types like list[str] or list[int].
    """
    with open(filepath) as f:
        # We split by whitespace to get a flat list of all tokens
        tokens: list[str] = f.read().strip().split()

    converted_values = {}
    token_idx = 0

    for field_name, field_type in schema:
        # Check if the type is a list (e.g., list[str], list[int])
        if get_origin(field_type) is list:
            # Extract the inner type (e.g., str from list[str])
            inner_type = get_args(field_type)[0]

            # Consume all remaining tokens for the list
            remaining_tokens = tokens[token_idx:]
            converted_values[field_name] = [inner_type(t) for t in remaining_tokens]

            # Since it's a list, we assume it's the last item or consumes the rest
            token_idx = len(tokens)
        else:
            # Handle single values
            if token_idx < len(tokens):
                converted_values[field_name] = field_type(tokens[token_idx])
                token_idx += 1

    return converted_values


def print_output(output: Any) -> None:
    """default prints using \n separator for lists or sets"""
    if isinstance(output, list) | isinstance(output, set):
        print(*output, sep="\n")

    else:
        print(output)
