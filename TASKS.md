# python-slugify — ETNA Tasks

Total tasks: 6

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `normalize_accents_twice_e52c35e3_1` | hypothesis | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 002 | `normalize_accents_twice_e52c35e3_1` | crosshair | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 003 | `stopwords_with_custom_separator_a1543fe0_1` | hypothesis | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 004 | `stopwords_with_custom_separator_a1543fe0_1` | crosshair | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 005 | `uppercase_pre_translations_a243ccdc_1` | hypothesis | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |
| 006 | `uppercase_pre_translations_a243ccdc_1` | crosshair | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |

## Witness Catalog

- `witness_nfkd_pre_normalize_case_math_italic` — U+1D41A 'mathematical bold a' must fold to 'a'
- `witness_nfkd_pre_normalize_case_double_struck` — U+1D552 'double-struck a' must fold to 'a'
- `witness_nfkd_pre_normalize_case_mixed` — mixed presentation forms + plain accented letters must all reach 'a'
- `witness_stopwords_respect_separator_case_space` — stopword 'the' with separator=' ' must still be stripped
- `witness_stopwords_respect_separator_case_underscore` — stopword 'a' with separator='_' must still be stripped
- `witness_add_uppercase_covers_case_two_pairs` — two distinct lowercase letters; both uppercase variants must be present
- `witness_add_uppercase_covers_case_cyrillic` — subset of CYRILLIC; checks 'я' and 'х' uppercase variants
