from typing import TypeVar, Generic

T = TypeVar('T')


class DSU(Generic[T]):
    """key data structure for Kruskal"""

    def __init__(self, items: list[T]) -> None:
        # initially each cell is its own root, and has rank 0
        self.root: dict[T, T] = {v: v for v in items}
        self.rank: dict[T, int] = {v: 0 for v in items}

    def find(self, item: T) -> T:
        if self.root[item] != item:
            self.root[item] = self.find(self.root[item])    # path compression
        return self.root[item]

    def union(self, item1: T, item2: T) -> None:
        root1: T = self.find(item1)
        root2: T = self.find(item2)
        if self.rank[root1] > self.rank[root2]:
            self.root[item2] = item1
        elif self.rank[root2] > self.rank[root1]:
            self.root[item1] = item2
        else:
            self.root[item1] = item2
            self.rank[item2] += 1

    def connected(self, item1: T, item2: T) -> bool:
        return self.find(item1) == self.find(item2)
