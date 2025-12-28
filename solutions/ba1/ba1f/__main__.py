from bio.utils import read_inputs
from bio.strings import argmins, skew
from typing import Any

import matplotlib.pyplot as plt


def parse_string(s: str) -> Any:
    return s


def main() -> None:
    args = read_inputs()

    # parse inputs
    genome = args[0]

    # run algorithm
    sk = skew(genome)

    print(*argmins(sk))
    plt.plot(sk)
    plt.show()


if __name__ == "__main__":
    main()
