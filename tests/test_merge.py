import sys

sys.path.append(".")
from fullstache import Fullstache


def test_ok():
    """This test should always pass"""
    pass


def test_words_fail():
    fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
    fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    assert fruits1 == fruits2


def test_numbers_fail():
    """Detects different numbers in a set"""
    number_to_text1 = {str(x): x for x in range(5)}
    number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    assert number_to_text1 == number_to_text2


def test_long_text_fail():
    """Is a text longer than it should?"""
    long_text = "Lorem ipsum dolor sit amet " * 10
    assert "hello world" in long_text
