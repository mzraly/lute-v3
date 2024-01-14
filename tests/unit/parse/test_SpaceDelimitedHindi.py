"""
Hindi language definition tests.

- Character substitutions: ´='|`='|’='|‘='|...=…|..=‥
- Split sentences at: .?!|।॥
- Split sentence exceptions: Mr.|Mrs.|Dr.|[A-Z].|Vd.|Vds.
- Word characters: a-zA-Z\u0900-\u0963\u0966-\u097F
"""

from lute.parse.space_delimited_parser import SpaceDelimitedParser

from .utils import parse_sentences


def test_empty(hindi):
    """test empty string handling"""

    actual = parse_sentences("", hindi, SpaceDelimitedParser)
    assert not actual


def test_spaces(hindi):
    """test retention of space characters"""

    actual = parse_sentences(" \t", hindi, SpaceDelimitedParser)
    assert actual == [[" \t"]]


def test_word(hindi):
    """test recognition of a word"""

    actual = parse_sentences("नमस्ते", hindi, SpaceDelimitedParser)
    assert actual == [["नमस्ते"]]


def test_word_then_comma(hindi):
    """test recognition of comma as a word separator"""

    actual = parse_sentences("नमसते,", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", ","]]


def test_word_then_period(hindi):
    """test recognition of period as a sentence terminator"""

    actual = parse_sentences("नमसते.", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", ".$"]]


def test_word_then_question(hindi):
    """test recognition of question mark as a sentence terminator"""

    actual = parse_sentences("नमसते?", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", "?$"]]


def test_word_then_faux_danda(hindi):
    """test recognition of ASCII vertical pipe being used to simulate Dev Nagari danda symbol"""

    actual = parse_sentences("नमसते|", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", "|$"]]


def test_word_then_real_danda(hindi):
    """test recognition of Dev Nagari danda symbol"""

    actual = parse_sentences("नमसते।", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", "।$"]]


def test_ellipsis_substitution(hindi):
    """test ellipsis substitution"""

    # Ellipsis substitution runs prior to sentence parsing
    # to avoid conflicting with sentence-terminator detection.
    actual = parse_sentences("नमसते...", hindi, SpaceDelimitedParser)
    assert actual == [["नमसते", "\u2026"]]


def test_hyphenated_word(english):
    """test hyphenated-word handling"""

    actual = parse_sentences("बारी-बारी", english, SpaceDelimitedParser)
    assert actual == [["बारी-बारी"]]


def test_sentences(hindi):
    """test breaking text into separate sentences"""

    actual = parse_sentences(
        # This is a short excerpt from असली अप्सरा
        # https://hindistory.net/story/82
        " ".join(
            [
                "जी हाँ, मैं आपको अप्सरा और चुड़ैल दोनों दिखा दूंगा ।",
                "कब ?",
                "बहुत जल्दी ।",
            ]
        ),
        hindi,
        SpaceDelimitedParser,
        maxcount=1,
    )
    assert actual == [
        [
            "जी",
            " ",
            "हाँ",
            ", ",
            "मैं",
            " ",
            "आपको",
            " ",
            "अप्सरा",
            " ",
            "और",
            " ",
            "चुड़ैल",
            " ",
            "दोनों",
            " ",
            "दिखा",
            " ",
            "दूंगा",
            " । $",
        ],
        [
            "कब",
            " ? $",
        ],
        [
            "बहुत",
            " ",
            "जल्दी",
            " ।$",
        ],
    ]
