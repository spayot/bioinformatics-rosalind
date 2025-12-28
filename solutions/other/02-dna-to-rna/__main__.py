import os
import sys

def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    
    print(s.replace("T","U"))



if __name__ == "__main__":
    main()
