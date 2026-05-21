def group_words(words):
    return reduce(
        lambda acc, word: (acc.setdefault(len(word), []).append(word) or acc),
        words,
        {},
    )


from pprint import pprint

pprint(group_words(["these", "are", "some", "words", "for", "grouping"]))
