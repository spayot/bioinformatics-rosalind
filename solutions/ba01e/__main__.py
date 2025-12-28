from bio.strings import find_clumps
from bio.utils import read_inputs


def main() -> None:
    args = read_inputs()
    
    # parse inputs
    genome = args[0]
    k, L, t = [int(arg) for arg in args[1:]]

    print(*find_clumps(genome, k, L, t))





if __name__ == "__main__":
    main()
