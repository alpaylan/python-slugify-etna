"""Property functions for the python-slugify ETNA workload.

Each property is pure, total, deterministic and returns a PropertyResult.
PASS when the invariant holds, fail(...) when violated. DISCARD when the
generated input does not satisfy the precondition the property checks.
"""
from __future__ import annotations

from typing import List, Tuple

from slugify import slugify
from slugify.special import add_uppercase_char

from ._result import DISCARD, PASS, PropertyResult, fail


# ---------------------------------------------------------------------------
# AddUppercaseCovers (variant: uppercase_pre_translations_a243ccdc_1)
# ---------------------------------------------------------------------------
def property_add_uppercase_covers(args: List[Tuple[str, str]]) -> PropertyResult:
    """``add_uppercase_char(pairs)`` must add the uppercase variant of every entry.

    Bug (mined from PR #148 / commit a243ccdc): pre-fix the ``return`` was
    indented inside the ``for`` loop, so the function returned after the
    first entry and dropped most uppercase variants.
    """
    pairs: List[Tuple[str, str]] = list(args)
    if not pairs:
        return DISCARD
    expected: List[Tuple[str, str]] = []
    for c, x in pairs:
        if not c or not x:
            return DISCARD
        if c.upper() != c:
            expected.append((c.upper(), x.capitalize()))
    if not expected:
        return DISCARD
    result = add_uppercase_char([(c, x) for c, x in pairs])
    missing = [p for p in expected if p not in result]
    if missing:
        return fail(
            f"add_uppercase_char({pairs!r}): missing uppercase variants {missing!r} "
            f"in result {result!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# StopwordsRespectSeparator (variant: stopwords_with_custom_separator_a1543fe0_1)
# ---------------------------------------------------------------------------
def property_stopwords_respect_separator(
    args: Tuple[List[str], str, str],
) -> PropertyResult:
    """``slugify(text, stopwords=[s], separator=sep)`` must drop ``s``.

    Bug (mined from commit a1543fe0): pre-fix the stopword block split the
    text on the user ``separator`` instead of the internal ``-``; with a
    non-default ``separator`` the split produced one big token and no
    stopword could ever match.
    """
    words, stopword, sep = args
    if not stopword or not sep or sep == "-":
        return DISCARD
    cleaned: List[str] = []
    for w in words:
        if not w or not w.isascii() or not w.isalnum():
            return DISCARD
        if stopword.lower() in w.lower():
            return DISCARD
        cleaned.append(w)
    if not cleaned:
        return DISCARD
    if not stopword.isascii() or not stopword.isalnum():
        return DISCARD
    text = " ".join(cleaned + [stopword] + cleaned)
    out = slugify(text, stopwords=[stopword], separator=sep)
    tokens = out.split(sep)
    if stopword.lower() in (t.lower() for t in tokens):
        return fail(
            f"slugify({text!r}, stopwords=[{stopword!r}], separator={sep!r}) "
            f"= {out!r}; stopword {stopword!r} still present as token"
        )
    return PASS


# ---------------------------------------------------------------------------
# CliRegexPatternForwarded (variant: regex_pattern_cli_ignored_7edf477f_1)
# ---------------------------------------------------------------------------
def property_cli_regex_pattern_forwarded(args: str) -> PropertyResult:
    """Parsing ``--regex-pattern P`` from argv must forward ``P`` into ``slugify_params``.

    Bug (mined from PR #175 / commit 7edf477f): ``slugify_params`` omitted
    ``regex_pattern=args.regex_pattern``, so the CLI flag was silently
    dropped before reaching ``slugify``.
    """
    pattern = args
    if not pattern or not pattern.isascii():
        return DISCARD
    if any(c in pattern for c in (" ", "\t", "\n", "=", "\x00")):
        return DISCARD
    from slugify.__main__ import parse_args, slugify_params
    # Use the ``--regex-pattern=<value>`` joined form so argparse does not
    # treat patterns that begin with ``-`` as a separate flag.
    ns = parse_args(["prog", f"--regex-pattern={pattern}", "hello"])
    params = slugify_params(ns)
    if "regex_pattern" not in params:
        return fail(
            f"slugify_params(parse_args([..., '--regex-pattern', {pattern!r}, ...])) "
            f"missing 'regex_pattern' key (got keys={sorted(params)!r})"
        )
    if params["regex_pattern"] != pattern:
        return fail(
            f"--regex-pattern {pattern!r} surfaced as "
            f"slugify_params['regex_pattern']={params['regex_pattern']!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# NfkdPreNormalize (variant: normalize_accents_twice_e52c35e3_1)
# ---------------------------------------------------------------------------
# Pre-composed presentation forms whose NFKD decomposition is exactly the
# ASCII letter; these expose the bug because ``unidecode`` cannot fold them
# without prior NFKD normalization.
_PRESENTATION_FORMS: List[Tuple[str, str]] = [
    ("\U0001D41A", "a"),  # MATHEMATICAL BOLD SMALL A
    ("\U0001D41B", "b"),  # MATHEMATICAL BOLD SMALL B
    ("\U0001D41C", "c"),  # MATHEMATICAL BOLD SMALL C
    ("\U0001D552", "a"),  # MATHEMATICAL DOUBLE-STRUCK SMALL A
    ("\U0001D553", "b"),  # MATHEMATICAL DOUBLE-STRUCK SMALL B
    ("\U0001D554", "c"),  # MATHEMATICAL DOUBLE-STRUCK SMALL C
    ("\U0001D586", "a"),  # MATHEMATICAL BOLD FRAKTUR SMALL A
    ("\U0001D5BA", "a"),  # MATHEMATICAL SANS-SERIF SMALL A
]


def property_nfkd_pre_normalize(args: int) -> PropertyResult:
    """Each pre-composed presentation Latin letter must fold to its ASCII base.

    Bug (mined from PR #143 / commit e52c35e3): pre-fix ``slugify`` did not
    NFKD-normalize before ``unidecode``; ``unidecode`` cannot map U+1D41A or
    similar pre-composed math letters and dropped them from the output.
    """
    idx = args % len(_PRESENTATION_FORMS)
    char, expected = _PRESENTATION_FORMS[idx]
    out = slugify(char)
    if out != expected:
        return fail(
            f"slugify({char!r}) = {out!r}; expected {expected!r} "
            f"(presentation form must NFKD-decompose before unidecode)"
        )
    return PASS
