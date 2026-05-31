from typing import TypeVar, Generic

T = TypeVar('T')

class DSU(Generic[T]):
    """key data structure for Kruskal"""
    
    def __init__(self, items: list[T]) -> None:
        # initially each cell is its own root, and has rank 0
        self.root: set = {v: v for v in items}
        self.rank: set = {v: 0 for v in items}

    def find(self, item: T) -> T:
        if self.root[item] != item:
            self.root[item] = self.find(self.root[item])    # path compression
        return self.root[item]

    def union(self, item1: T, item2: T) -> None:
        if self.rank[item1] > self.rank[item2]:
            self.root[item2] = item1
        elif self.rank[item2] > self.rank[item1]:
            self.root[item1] = item2
        else:
            self.root[item1] = item2
            self.rank[item2] += 1

    def connected(self, item1: T, item2: T) -> bool:
        return self.find(item1) == self.find(item2)

            