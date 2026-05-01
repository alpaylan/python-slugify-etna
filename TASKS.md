# python-slugify — ETNA Tasks

Total tasks: 16

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `normalize_accents_twice_e52c35e3_1` | proptest | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 002 | `normalize_accents_twice_e52c35e3_1` | quickcheck | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 003 | `normalize_accents_twice_e52c35e3_1` | crabcheck | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 004 | `normalize_accents_twice_e52c35e3_1` | hegel | `NfkdPreNormalize` | `witness_nfkd_pre_normalize_case_math_italic` |
| 005 | `regex_pattern_cli_ignored_7edf477f_1` | proptest | `CliRegexPatternForwarded` | `witness_cli_regex_pattern_forwarded_case_basic` |
| 006 | `regex_pattern_cli_ignored_7edf477f_1` | quickcheck | `CliRegexPatternForwarded` | `witness_cli_regex_pattern_forwarded_case_basic` |
| 007 | `regex_pattern_cli_ignored_7edf477f_1` | crabcheck | `CliRegexPatternForwarded` | `witness_cli_regex_pattern_forwarded_case_basic` |
| 008 | `regex_pattern_cli_ignored_7edf477f_1` | hegel | `CliRegexPatternForwarded` | `witness_cli_regex_pattern_forwarded_case_basic` |
| 009 | `stopwords_with_custom_separator_a1543fe0_1` | proptest | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 010 | `stopwords_with_custom_separator_a1543fe0_1` | quickcheck | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 011 | `stopwords_with_custom_separator_a1543fe0_1` | crabcheck | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 012 | `stopwords_with_custom_separator_a1543fe0_1` | hegel | `StopwordsRespectSeparator` | `witness_stopwords_respect_separator_case_space` |
| 013 | `uppercase_pre_translations_a243ccdc_1` | proptest | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |
| 014 | `uppercase_pre_translations_a243ccdc_1` | quickcheck | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |
| 015 | `uppercase_pre_translations_a243ccdc_1` | crabcheck | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |
| 016 | `uppercase_pre_translations_a243ccdc_1` | hegel | `AddUppercaseCovers` | `witness_add_uppercase_covers_case_two_pairs` |

## Witness Catalog

- `witness_nfkd_pre_normalize_case_math_italic` — U+1D41A 'mathematical bold a' must fold to 'a'
- `witness_nfkd_pre_normalize_case_double_struck` — U+1D552 'double-struck a' must fold to 'a'
- `witness_nfkd_pre_normalize_case_mixed` — mixed presentation forms + plain accented letters must all reach 'a'
- `witness_cli_regex_pattern_forwarded_case_basic` — --regex-pattern X must surface as kwargs['regex_pattern'] == 'X'
- `witness_cli_regex_pattern_forwarded_case_underscore` — single-character pattern still forwarded
- `witness_stopwords_respect_separator_case_space` — stopword 'the' with separator=' ' must still be stripped
- `witness_stopwords_respect_separator_case_underscore` — stopword 'a' with separator='_' must still be stripped
- `witness_add_uppercase_covers_case_two_pairs` — two distinct lowercase letters; both uppercase variants must be present
- `witness_add_uppercase_covers_case_cyrillic` — subset of CYRILLIC; checks 'я' and 'х' uppercase variants
