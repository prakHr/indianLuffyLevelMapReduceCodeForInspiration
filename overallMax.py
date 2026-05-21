def map_combination(left, right):
    return left + right


def keep_if_even(acc, nxt):
    if nxt % 2 == 0:
        return acc + [nxt]
    else:
        return acc


def keep_if_odd(acc, nxt):
    if nxt % 2 == 1:
        return acc + [nxt]
    else:
        return acc


def get_list(acc, nxt):
    return acc + [nxt]


def my_max(acc, nxt):
    return max(acc, nxt)
INF = pow(10,32)
def get_overall_max(list_of_lists):
    ans = -1*INF
    for xs in list_of_lists:
        ans = reduce(my_max, xs, ans)
    return ans


def get_list_of_evens(list_of_lists):
    ans = []
    for xs in list_of_lists:
        ans = reduce(get_list, xs, ans)
        # ans = reduce(keep_if_even, xs, ans)
    return ans


list_of_lists = [[2] * 100 for _ in range(100)]
print(*get_list_of_evens(list_of_lists))
