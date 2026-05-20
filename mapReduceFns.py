from functools import reduce


def my_add(left, right):
    return left + right


def reduce_sum_of_lists(list_of_lists):
    ans = 0
    for xs in list_of_lists:
        ans = reduce(my_add, xs, ans)
    return ans


# list_of_lists = [[3, 4] * 1000_00000 for _ in range(1)]
# print(reduce_sum_of_lists(list_of_lists))


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


from functools import reduce


def get_n_largest(seq, n):
    return sorted(seq, reverse=True)[:n]
    # return reduce(lambda acc, x: sorted(acc + [x], reverse=True)[:n], seq, [])


def get_n_smallest(seq, n):
    return sorted(seq, reverse=False)[:n]
    # return reduce(lambda acc, x: sorted(acc + [x])[:n], seq, [])


# nums = [1, 12]
# n = 1
# print("N largest:", *get_n_largest(nums, n))
# print("N smallest:", *get_n_smallest(nums, n))


def group_words(words):
    return reduce(
        lambda acc, word: (acc.setdefault(len(word), []).append(word) or acc),
        words,
        {},
    )


# from pprint import pprint

# pprint(group_words(["these", "are", "some", "words", "for", "grouping"]))


def get_list_of_evens(list_of_lists):
    ans = []
    for xs in list_of_lists:
        ans = reduce(get_list, xs, ans)
        # ans = reduce(keep_if_even, xs, ans)
    return ans


# list_of_lists = [[2] * 100 for _ in range(100)]
# print(*get_list_of_evens(list_of_lists))
