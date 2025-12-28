import os
import sys

COMPLEMENTS = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}
def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    sc = [COMPLEMENTS[char] for char in s.strip()[::-1]] 
    print("".join(sc))



if __name__ == "__main__":
    main()
