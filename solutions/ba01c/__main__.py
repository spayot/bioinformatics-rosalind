import os
import sys

from bio.strings import reverse_complement

def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    
    pattern = s.strip()
    
    print(reverse_complement(pattern))


if __name__ == "__main__":
    main()
