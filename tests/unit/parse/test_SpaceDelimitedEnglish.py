"""
English language definition tests.

- Character substitutions: ´='|`='|’='|‘='|...=…|..=‥
- Split sentences at: .!?
- Split sentence exceptions: Mr.|Mrs.|Dr.|[A-Z].|Vd.|Vds.
- Word characters: a-zA-ZÀ-ÖØ-öø-ȳáéíóúÁÉÍÓÚñÑ
"""

from lute.parse.space_delimited_parser import SpaceDelimitedParser

from .utils import parse_sentences


def test_empty(english):
    """test empty string handling"""

    actual = parse_sentences("", english, SpaceDelimitedParser)
    assert not actual


def test_spaces(english):
    """test retention of space characters"""

    actual = parse_sentences(" \t", english, SpaceDelimitedParser)
    assert actual == [[" \t"]]


def test_word(english):
    """test recognition of a word"""

    actual = parse_sentences("hello", english, SpaceDelimitedParser)
    assert actual == [["hello"]]


def test_word_then_comma(english):
    """test recognition of comma as a word separator"""

    actual = parse_sentences("hello,", english, SpaceDelimitedParser)
    assert actual == [["hello", ","]]


def test_word_then_period(english):
    """test recognition of period as a sentence terminator"""

    actual = parse_sentences("hello.", english, SpaceDelimitedParser)
    assert actual == [["hello", ".$"]]


def test_word_then_question(english):
    """test recognition of question mark as a sentence terminator"""

    actual = parse_sentences("hello?", english, SpaceDelimitedParser)
    assert actual == [["hello", "?$"]]


def test_contraction(english):
    """test contraction handling"""

    actual = parse_sentences("Don't!!!", english, SpaceDelimitedParser)
    assert actual == [["Don", "'", "t", "!!!$"]]
    # NOTE: Would prefer this:
    #   assert actual == [["Don't", "!!!$"]]


def test_dieresis(english):
    """test dieresis handling"""

    actual = parse_sentences("naïve zoölogist", english, SpaceDelimitedParser)
    assert actual == [["naïve", " ", "zoölogist"]]


def test_ellipsis_substitution(english):
    """test ellipsis substitution"""

    # Ellipsis substitution runs prior to sentence parsing
    # to avoid conflicting with sentence-terminator detection.
    actual = parse_sentences("Well...", english, SpaceDelimitedParser)
    assert actual == [["Well", "\u2026"]]


def test_hyphenated_word(english):
    """test hyphenated-word handling"""

    actual = parse_sentences("teeter-totter", english, SpaceDelimitedParser)
    assert actual == [["teeter", "-", "totter"]]
    # NOTE: Would prefer this:
    #   assert actual == [["teeter-totter"]]


def test_number_with_suffix(english):
    """test numbers with ordinal and unit suffixes"""

    # In English there are at least two use cases for numbers with text suffixes:
    # 1. Ordinal numbers, e.g. 1st, 2nd, 3rd, 4th, ...
    # 2. Units of measure, eg 26.6mi, 7lb, -40C, ...
    # It's better to treat the suffixes as separate words; otherwise
    # we end up with a new term for each (number, suffix) combination.
    actual = parse_sentences("42nd", english, SpaceDelimitedParser)
    assert actual == [["42", "nd"]]


def test_split_sentence_exceptions(english):
    """test not splitting sentences after configured exceptions"""

    actual = parse_sentences("Mr. Frost & A.E. Housman", english, SpaceDelimitedParser)
    assert actual == [["Mr.", " ", "Frost", " & ", "A.", "E.", " ", "Housman"]]


def test_unicode_quotes(english):
    """test unicode quote handling"""

    actual = parse_sentences(
        "“Less work,” Peter offered", english, SpaceDelimitedParser
    )
    assert actual == [["“", "Less", " ", "work", ",” ", "Peter", " ", "offered"]]


def test_sentences(english):
    """test breaking text into separate sentences"""

    actual = parse_sentences(
        # This is a short excerpt from The Count of Monte-Cristo
        # https://www.gutenberg.org/cache/epub/1184/pg1184-images.html
        " ".join(
            [
                "Morrel looked around him, and then, drawing Dantès on one side, he said suddenly—",
                "“And how is the emperor?”",
                "“Very well, as far as I could judge from the sight of him.”",
                "“You saw the emperor, then?”",
            ]
        ),
        english,
        SpaceDelimitedParser,
        maxcount=1,
    )
    assert actual == [
        [
            "Morrel",
            " ",
            "looked",
            " ",
            "around",
            " ",
            "him",
            ", ",
            "and",
            " ",
            "then",
            ", ",
            "drawing",
            " ",
            "Dantès",
            " ",
            "on",
            " ",
            "one",
            " ",
            "side",
            ", ",
            "he",
            " ",
            "said",
            " ",
            "suddenly",
            "— “",
            "And",
            " ",
            "how",
            " ",
            "is",
            " ",
            "the",
            " ",
            "emperor",
            "?” “$",
        ],
        [
            "Very",
            " ",
            "well",
            ", ",
            "as",
            " ",
            "far",
            " ",
            "as",
            " ",
            "I",
            " ",
            "could",
            " ",
            "judge",
            " ",
            "from",
            " ",
            "the",
            " ",
            "sight",
            " ",
            "of",
            " ",
            "him",
            ".” “$",
        ],
        [
            "You",
            " ",
            "saw",
            " ",
            "the",
            " ",
            "emperor",
            ", ",
            "then",
            "?”$",
        ],
    ]
