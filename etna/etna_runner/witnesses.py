"""Concrete witnesses for the python-slugify ETNA workload.

Each ``witness_<snake>_case_<tag>`` is a no-arg function that calls
``property_<snake>`` with frozen inputs. On the base tree every witness
returns PASS; with the corresponding patch reverse-applied, the witness
returns fail(...).
"""
from __future__ import annotations

from . import properties
from ._result import PropertyResult


# ---------------------------------------------------------------------------
# uppercase_pre_translations_a243ccdc_1
# ---------------------------------------------------------------------------
def witness_add_uppercase_covers_case_two_pairs() -> PropertyResult:
    # Two distinct lowercase letters → both uppercase variants must appear.
    return properties.property_add_uppercase_covers([("a", "alpha"), ("b", "beta")])


def witness_add_uppercase_covers_case_cyrillic() -> PropertyResult:
    # Subset of the real CYRILLIC table; covers the second/third entries
    # which the buggy version drops because it returns after the first.
    return properties.property_add_uppercase_covers([
        ("ё", "e"),    # ё
        ("я", "ya"),   # я
        ("х", "h"),    # х
    ])


# ---------------------------------------------------------------------------
# stopwords_with_custom_separator_a1543fe0_1
# ---------------------------------------------------------------------------
def witness_stopwords_respect_separator_case_space() -> PropertyResult:
    return properties.property_stopwords_respect_separator(
        (["quick", "brown", "fox"], "the", " ")
    )


def witness_stopwords_respect_separator_case_underscore() -> PropertyResult:
    return properties.property_stopwords_respect_separator(
        (["small", "world"], "of", "_")
    )


# ---------------------------------------------------------------------------
# regex_pattern_cli_ignored_7edf477f_1
# ---------------------------------------------------------------------------
def witness_cli_regex_pattern_forwarded_case_basic() -> PropertyResult:
    return properties.property_cli_regex_pattern_forwarded("abc")


def witness_cli_regex_pattern_forwarded_case_underscore() -> PropertyResult:
    return properties.property_cli_regex_pattern_forwarded("z")


# ---------------------------------------------------------------------------
# normalize_accents_twice_e52c35e3_1
# ---------------------------------------------------------------------------
def witness_nfkd_pre_normalize_case_math_italic() -> PropertyResult:
    # Index 0 of the table → MATHEMATICAL BOLD SMALL A (U+1D41A).
    return properties.property_nfkd_pre_normalize(0)


def witness_nfkd_pre_normalize_case_double_struck() -> PropertyResult:
    # Index 3 of the table → MATHEMATICAL DOUBLE-STRUCK SMALL A (U+1D552).
    return properties.property_nfkd_pre_normalize(3)


def witness_nfkd_pre_normalize_case_mixed() -> PropertyResult:
    # Index 6 of the table → MATHEMATICAL BOLD FRAKTUR SMALL A (U+1D586).
    return properties.property_nfkd_pre_normalize(6)
