import os
import sys
from collections import Counter

def main():
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    c = Counter(s)
    counts = [str(c[char]) for char in "ACGT"]
    print(f"dna length: {len(s)}")
    print(" ".join(counts))



if __name__ == "__main__":
    main()
