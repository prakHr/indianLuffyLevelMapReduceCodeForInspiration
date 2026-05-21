from functools import reduce

def combine_counts(left, right):
    unique_keys = set(left.keys()).union(set(right.keys()))
    return {k: left.get(k, 0) + right.get(k, 0) for k in unique_keys}


def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt, 0) + 1
    return acc


def my_frequencies(list_of_strings):
    f_acc = make_counts
    f_com = combine_counts
    res = {}
    for s in list_of_strings:
        res = f_com(res, reduce(f_acc, s, {}))
    return res
    

xs = "miss"
ys = "iss"
zs = "ippi"
list_of_strings = [xs,ys,zs]
res = my_frequencies(list_of_strings)
print(res)
