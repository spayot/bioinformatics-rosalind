import os
import sys

def pattern_count(text: str, pattern: str) -> int:
    print(f"{text=} {pattern=}")
    count = 0
    k = len(pattern)
    for i in range(len(text) - k + 1):
        count += (text[i:i+k] == pattern)                  
    return count

def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    
    text, pattern = s.split()
    print(f"{pattern_count(text, pattern)=}")




if __name__ == "__main__":
    main()
