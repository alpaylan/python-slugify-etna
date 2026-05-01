"""Hypothesis strategies for the python-slugify ETNA workload.

CrossHair-compatible: stick to ``st.integers``, ``st.text``, ``st.lists``,
``st.tuples``, ``st.sampled_from``. No custom ``@composite`` strategies.
"""
from __future__ import annotations

from hypothesis import strategies as st


# Lowercase ASCII letters whose ``.upper()`` differs from themselves; pairs
# them with a small ASCII translation. Covers the ``add_uppercase_char``
# property without dragging unicode normalisation into the test space.
_LOWERCASE_LETTER = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=1
)
_TRANSLATION = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=3
)


def strategy_add_uppercase_covers():
    return st.lists(
        st.tuples(_LOWERCASE_LETTER, _TRANSLATION),
        min_size=1,
        max_size=4,
        unique_by=lambda p: p[0],
    )


# Plain ASCII alphanumeric word fragments (no spaces, no dashes), used as
# the surrounding tokens around a stopword. Hypothesis-only filters keep
# them disjoint from the stopword.
_WORD = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=4
)
_STOPWORD = st.sampled_from(["the", "and", "of", "in", "to"])
_NON_DEFAULT_SEPARATOR = st.sampled_from([" ", "_", ".", "+", ":"])


def strategy_stopwords_respect_separator():
    return st.tuples(
        st.lists(_WORD, min_size=1, max_size=3),
        _STOPWORD,
        _NON_DEFAULT_SEPARATOR,
    )


# A short ASCII regex pattern body, restricted to characters that argparse
# can handle without quoting and that survive shell-like tokenization.
_PATTERN_CHAR = st.sampled_from(list("abcdefghijklmnopqrstuvwxyz0123456789-^[]"))


def strategy_cli_regex_pattern_forwarded():
    return st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789-^[]",
                   min_size=1, max_size=8)


def strategy_nfkd_pre_normalize():
    # Index into the table of presentation-form letters; the property mods
    # by the table length so any non-negative int is fine.
    return st.integers(min_value=0, max_value=255)
