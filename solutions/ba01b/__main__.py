import os
import sys

from bio.strings import most_frequent_kmers


def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    
    text, k = s.split("\n")[:2]
    
    print(" ".join(most_frequent_kmers(text, int(k))))



if __name__ == "__main__":
    main()
