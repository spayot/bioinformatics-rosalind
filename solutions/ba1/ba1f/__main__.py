import sys
from bio.utils import read_inputs
from bio.strings import argmins, skew
from typing import Any

import matplotlib.pyplot as plt


def parse_string(s: str) -> Any:
    return s


def main() -> None:
    schema = [("genome", str)]
    args = read_inputs(filepath=sys.argv[1], schema=schema)

    # run algorithm
    sk = skew(**args)

    print(*argmins(sk))
    plt.plot(sk)
    plt.show()


if __name__ == "__main__":
    main()
