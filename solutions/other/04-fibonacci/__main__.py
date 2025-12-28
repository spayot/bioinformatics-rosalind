import os
import sys

def fibonacci(n: int, k: int) -> int:
    match n:
        case 1:
            return 1
        case 2:
            return 1
    return fibonacci(n-1, k) + k* fibonacci(n - 2, k)

def fibonacci2(n: int, k: int) -> int:
    fn, fn_ = 1, 1
    
    for _ in range(2, n):
        tmp = fn
        fn = fn + k * fn_
        fn_ = tmp
    return fn

def main() -> None:
    with open(os.path.join(sys.argv[0], sys.argv[1])) as f:
        s = f.read()
    n, k = [int(x) for x in s.split()]
    
    print(fibonacci2(n, k))



if __name__ == "__main__":
    main()
