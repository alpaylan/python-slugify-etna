# python-slugify — Injected Bugs

Slug-from-Unicode-text library — bug variants hand-crafted against modern HEAD, drawing from upstream history (un33k/python-slugify).

Total mutations: 3

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `normalize_accents_twice_e52c35e3_1` | `normalize_accents_twice` | `slugify/slugify.py:120` | `patch` | `e52c35e34899bc21a389aa7f4fe5084423cf538c` |
| 2 | `stopwords_with_custom_separator_a1543fe0_1` | `stopwords_with_custom_separator` | `slugify/slugify.py:180` | `patch` | `a1543fe0ae019606bec660d6cf2e70a435ff29e4` |
| 3 | `uppercase_pre_translations_a243ccdc_1` | `uppercase_pre_translations` | `slugify/special.py:7` | `patch` | `a243ccdc6d2b650b83782e03893e8f117356aeff` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `normalize_accents_twice_e52c35e3_1` | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic`, `witness_nfkd_pre_normalize_case_double_struck`, `witness_nfkd_pre_normalize_case_mixed` |
| `stopwords_with_custom_separator_a1543fe0_1` | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space`, `witness_stopwords_respect_separator_case_underscore` |
| `uppercase_pre_translations_a243ccdc_1` | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs`, `witness_add_uppercase_covers_case_cyrillic` |

## Framework Coverage

| Property | proptest | quickcheck | crabcheck | hegel |
|----------|---------:|-----------:|----------:|------:|
| `NfkdPreNormalize` | ✓ | ✓ | ✓ | ✓ |
| `StopwordsRespectSeparator` | ✓ | ✓ | ✓ | ✓ |
| `AddUppercaseCovers` | ✓ | ✓ | ✓ | ✓ |

## Bug Details

### 1. normalize_accents_twice

- **Variant**: `normalize_accents_twice_e52c35e3_1`
- **Location**: `slugify/slugify.py:120` (inside `slugify`)
- **Property**: `NfkdPreNormalize`
- **Witness(es)**:
  - `witness_nfkd_pre_normalize_case_math_italic` — U+1D41A 'mathematical bold a' must fold to 'a'
  - `witness_nfkd_pre_normalize_case_double_struck` — U+1D552 'double-struck a' must fold to 'a'
  - `witness_nfkd_pre_normalize_case_mixed` — mixed presentation forms + plain accented letters must all reach 'a'
- **Source**: [#143](https://github.com/un33k/python-slugify/pull/143), internal — Ci - Normalize accented text twice. (#143)
  > ``slugify`` historically called ``unidecode()`` on the raw input. ``unidecode`` only handles single code points, so pre-composed presentation forms (mathematical italic / double-struck letters, e.g. U+1D41A ``𝐚`` or U+1D552 ``𝕒``) were dropped to the empty slug instead of folding to ``a``. The fix prepends a ``unicodedata.normalize('NFKD', text)`` (or ``'NFKC'`` when ``allow_unicode``) so the presentation forms decompose to their ASCII bases first.
- **Fix commit**: `e52c35e34899bc21a389aa7f4fe5084423cf538c` — Ci - Normalize accented text twice. (#143)
- **Invariant violated**: For each character ``c`` in input whose NFKD decomposition contains an ASCII letter ``L``, ``slugify(c)`` contains ``L`` (or its lowercase form). In particular, ``slugify('𝐚𝕒')`` is non-empty.
- **How the mutation triggers**: The mutation removes the pre-``unidecode`` ``NFKD``/``NFKC`` normalization pass. Pre-composed presentation forms reach ``unidecode`` undecomposed; ``unidecode`` returns the empty string for them, and they vanish from the output.

### 2. stopwords_with_custom_separator

- **Variant**: `stopwords_with_custom_separator_a1543fe0_1`
- **Location**: `slugify/slugify.py:180` (inside `slugify`)
- **Property**: `StopwordsRespectSeparator`
- **Witness(es)**:
  - `witness_stopwords_respect_separator_case_space` — stopword 'the' with separator=' ' must still be stripped
  - `witness_stopwords_respect_separator_case_underscore` — stopword 'a' with separator='_' must still be stripped
- **Source**: internal — fixed stopword replacement bug (different separators)
  > Stopword stripping happens after the text is already normalized to use ``DEFAULT_SEPARATOR`` (``-``). Pre-fix the code split and re-joined the text on the user-supplied ``separator`` instead of ``DEFAULT_SEPARATOR``; with any non-default separator the split misfired and stopwords were never removed.
- **Fix commit**: `a1543fe0ae019606bec660d6cf2e70a435ff29e4` — fixed stopword replacement bug (different separators)
- **Invariant violated**: If a stopword appears as a whole token in the input and is included in ``stopwords=[...]``, ``slugify(text, stopwords=..., separator=sep)`` does not contain that stopword as a token in the result, regardless of ``sep``.
- **How the mutation triggers**: The mutation replaces ``DEFAULT_SEPARATOR`` with ``separator`` inside the stopword block. With ``separator != '-'`` the split returns the whole text as a single token (no '-' boundaries appear in the user-visible separator), so the stopword filter cannot match anything.

### 3. uppercase_pre_translations

- **Variant**: `uppercase_pre_translations_a243ccdc_1`
- **Location**: `slugify/special.py:7` (inside `add_uppercase_char`)
- **Property**: `AddUppercaseCovers`
- **Witness(es)**:
  - `witness_add_uppercase_covers_case_two_pairs` — two distinct lowercase letters; both uppercase variants must be present
  - `witness_add_uppercase_covers_case_cyrillic` — subset of CYRILLIC; checks 'я' and 'х' uppercase variants
- **Source**: [#148](https://github.com/un33k/python-slugify/pull/148), internal — fix uppercase pre-translations (#148)
  > ``add_uppercase_char`` walks a per-language replacement list and inserts the uppercase variant of every entry. Pre-fix the ``return char_list`` was indented one level too deep so the function returned after processing the first entry, leaving the bulk of the uppercase variants out of ``PRE_TRANSLATIONS``.
- **Fix commit**: `a243ccdc6d2b650b83782e03893e8f117356aeff` — fix uppercase pre-translations (#148)
- **Invariant violated**: After ``add_uppercase_char(pairs)``, for every original ``(c, x)`` in ``pairs`` whose ``c.upper() != c``, the pair ``(c.upper(), x.capitalize())`` is in the result.
- **How the mutation triggers**: The mutation re-indents ``return char_list`` so it lives inside the ``for`` loop. The function returns after the first iteration and only the first entry's uppercase variant is inserted; subsequent entries are silently dropped.
