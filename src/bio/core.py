class Kmer(str):
    @property
    def k(self) -> int:
        return len(self)

    @property
    def suffix(self) -> str:
        return self[1:]

    @property
    def prefix(self) -> str:
        return self[:-1]
