from functools import reduce
from heapq import heappush, heappushpop
import random


def top_k(xs, k):
    def reducer(heap, x):
        if len(heap) < k:
            heappush(heap, x)
        else:
            heappushpop(heap, x)

        return heap

    return sorted(reduce(reducer, xs, []), reverse=True)


# xs = {random.randint(1, 1000000000) for _ in range(1000000)}

# print(top_k(xs, 500))


def smallest_k(xs, k):
    def reducer(heap, x):
        x = -x

        if len(heap) < k:
            heappush(heap, x)
        else:
            heappushpop(heap, x)

        return heap

    return sorted([-x for x in reduce(reducer, xs, [])])


# xs = {random.randint(1, 1000000000) for _ in range(1000000)}

# print(smallest_k(xs, 500))
