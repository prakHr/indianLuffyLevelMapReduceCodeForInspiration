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
