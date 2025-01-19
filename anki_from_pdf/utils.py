from typing import List, Tuple, Any


def unzip(xys: List[Tuple[Any, Any]]) -> Tuple[List[Any], List[Any]]:
    xs = [x for x, y in xys]
    ys = [y for x, y in xys]
    return xs, ys


def flatten(xxs: List[List[Any]]) -> List[Any]:
    return [x for xs in xxs for x in xs]
