"""
Parser unit test utilities.
"""

from lute.parse.base import SentenceGroupIterator


# Default value for maxcount is 1 to ensure each sentence is returned as a separate list item.
def parse_sentences(text, language, parser, maxcount=1):
    """
    Parse text using given language, parser constructor, and sentence iterator maxcount value.
    Return a list of lists, one list per sentence group, a string for each token with $ appended
    if the token marks the end of a sentence.
    """
    parser_object = parser()
    tokens = parser_object.get_parsed_tokens(text, language)
    groups = []
    it = SentenceGroupIterator(tokens, maxcount)
    while group := it.next():
        items = []
        for g in group:
            prefix = g.token
            suffix = "$" if g.is_end_of_sentence else ""
            items.append(f"{prefix}{suffix}")
        groups.append(items)
    return groups
