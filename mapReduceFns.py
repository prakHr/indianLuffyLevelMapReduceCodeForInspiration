'''
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

'''
'''
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
'''

'''
import asyncio
import random
from urllib import parse
from itertools import chain

import aiohttp


def link_to_title(link):
    return link["title"]


def clean_if_key(page, key):
    if key in page:
        return [link_to_title(x) for x in page[key]]
    return []


async def get_wiki_links(pageTitle, session, semaphore):

    async with semaphore:

        safe_title = parse.quote(pageTitle)

        url = (
            "https://en.wikipedia.org/w/api.php"
            "?action=query"
            "&prop=links|linkshere"
            "&pllimit=100"
            "&lhlimit=100"
            f"&titles={safe_title}"
            "&format=json"
            "&formatversion=2"
        )

        for attempt in range(5):

            try:

                # small random delay prevents synchronized bursts
                await asyncio.sleep(
                    random.uniform(0.2, 0.8)
                )

                async with session.get(
                    url,
                    timeout=15
                ) as response:

                    if response.status == 429:

                        wait_time = (
                            (2 ** attempt)
                            + random.uniform(0, 1)
                        )

                        print(
                            f"Rate limited: {pageTitle}"
                            f" retry in {wait_time:.1f}s"
                        )

                        await asyncio.sleep(wait_time)
                        continue

                    response.raise_for_status()

                    data = await response.json()

                page = data["query"]["pages"][0]

                inbound = clean_if_key(
                    page,
                    "links"
                )

                outbound = clean_if_key(
                    page,
                    "linkshere"
                )

                return {
                    "title": pageTitle,
                    "in-links": inbound,
                    "out-links": outbound
                }

            except Exception as e:

                print(
                    f"Error fetching "
                    f"{pageTitle}: {e}"
                )

                return {
                    "title": pageTitle,
                    "in-links": [],
                    "out-links": []
                }

        print(f"Skipping {pageTitle}")

        return {
            "title": pageTitle,
            "in-links": [],
            "out-links": []
        }


def flatten_network(page):
    return (
        page["in-links"]
        + page["out-links"]
    )


def page_to_edges(page):

    outgoing = [
        (page["title"], p)
        for p in page["out-links"]
    ]

    incoming = [
        (p, page["title"])
        for p in page["in-links"]
    ]

    return outgoing + incoming


async def main():

    headers = {
        "User-Agent":
        "WikiGraphCrawler/1.0 "
        "(contact: your_email@example.com)"
    }

    # only allow 2 simultaneous requests
    semaphore = asyncio.Semaphore(2)

    async with aiohttp.ClientSession(
        headers=headers
    ) as session:

        print(
            "Fetching root page..."
        )

        root = await get_wiki_links(
            "Parallel_computing",
            session,
            semaphore
        )

        initial_network = flatten_network(
            root
        )

        print(
            f"Found "
            f"{len(initial_network)} pages"
        )

        print(
            initial_network[:10]
        )

        tasks = [

            get_wiki_links(
                page,
                session,
                semaphore
            )

            for page in initial_network
        ]

        print(
            "Fetching network..."
        )

        all_pages = await asyncio.gather(
            *tasks
        )

        print(
            "Building edges..."
        )

        edges = [

            page_to_edges(page)

            for page in all_pages
        ]

        edges = list(
            chain.from_iterable(
                edges
            )
        )

        print(
            f"Total edges: "
            f"{len(edges)}"
        )
        

        # Optional graph export

        # import networkx as nx
        #
        # G = nx.DiGraph()
        # G.add_edges_from(edges)
        #
        # nx.write_gexf(
        #     G,
        #     "MyGraph.gexf"
        # )


if __name__ == "__main__":
    asyncio.run(main())
'''
'''
import re


class PhoneFormatter:
    def __init__(self):
        self.r = re.compile(r"\d")

    def pretty_format(self, phone_number):
        phone_numbers = self.r.findall(phone_number)
        area_code = "".join(phone_numbers[-10:-7])
        first_3 = "".join(phone_numbers[-7:-4])
        last_4 = "".join(phone_numbers[-4 : len(phone_numbers)])
        return "({}) {}-{}".format(area_code, first_3, last_4)


phone_numbers = ["(123) 456-7890", "1234567890", "123.456.7890", "+1 123 456-7890"]

P = PhoneFormatter()
print(list(map(P.pretty_format, phone_numbers)))
'''
'''

from functools import reduce


def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt, 0) + 1
    return acc


def my_frequencies(xs):
    return reduce(make_counts, xs, {})


xs = ["A", "B", "C", "A", "A", "C", "A"]
ys = [1, 3, 6, 1, 2, 9, 3, 12]

print(my_frequencies(xs))
print(my_frequencies(ys))
print(my_frequencies("mississippi"))


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


def get_n_smallest(seq, n):
    return sorted(seq, reverse=False)[:n]


nums = [1, 12]
n = 1
print("N largest:", *get_n_largest(nums, n))
print("N smallest:", *get_n_smallest(nums, n))


def group_words(words):
    return reduce(
        lambda acc, word: (acc.setdefault(len(word), []).append(word) or acc),
        words,
        {},
    )


from pprint import pprint

pprint(group_words(["these", "are", "some", "words", "for", "grouping"]))


def get_list_of_evens(list_of_lists):
    ans = []
    for xs in list_of_lists:
        ans = reduce(get_list, xs, ans)
        # ans = reduce(keep_if_even, xs, ans)
    return ans


list_of_lists = [[2] * 100 for _ in range(100)]
print(*get_list_of_evens(list_of_lists))
'''
