from bio.utils import read_inputs

from bio.strings import find_all_occurences

def main() -> None:
    
    pattern, text = read_inputs()

    print(*(str(i) for i in find_all_occurences(pattern, text)))



if __name__ == "__main__":
    main()
