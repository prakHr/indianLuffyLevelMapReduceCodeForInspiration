
from functools import reduce


def my_add(left, right):
    return left + right


def reduce_sum_of_lists(list_of_lists):
    ans = 0
    for xs in list_of_lists:
        ans = reduce(my_add, xs, ans)
    return ans


list_of_lists = [[3, 4] * 1000_00000 for _ in range(1)]
print(reduce_sum_of_lists(list_of_lists))
