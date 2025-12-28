import os
import sys

from dataclasses import dataclass
# from ..utils import timeit

from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@dataclass
class DnaString:
    idx: str
    string: str
    gc_content: float

    @classmethod
    def from_fasta(cls, s: str):
       idx, string = s.split("\n", maxsplit=1)
       string = string.replace("\n", "")
       gc_content = len([c for c in string if c in "GC"]) / len(string) * 100
       return cls(idx, string, gc_content)



@timeit
def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    
    dna_strings = s.split(">")[1:]

    m = 0
    idx = None

    for string in dna_strings:
        ds = DnaString.from_fasta(string)
        # print(ds)
        if ds.gc_content > m:
            m = ds.gc_content
            idx = ds.idx

    print(idx, m, sep="\n")

    



if __name__ == "__main__":
    main()
