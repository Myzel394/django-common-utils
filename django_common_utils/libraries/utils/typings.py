from typing import *

T = TypeVar("T")
S = TypeVar("S")

__all__ = [
    "EnsureIterationType", "EnsureIterationDictType"
]

EnsureIterationType = Tuple[Iterable[T], T]
EnsureIterationDictType = Dict[EnsureIterationType[T], EnsureIterationType[S]]
