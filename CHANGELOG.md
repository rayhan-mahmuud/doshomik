# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Walking skeleton: package structure, exceptions (`DoshomikError`, `ParseError`, `FormatError`), CI/CD workflows, and stub public API.
- Phase 2 — parser: `_constants.py` (digit/multiplier/currency maps), `_tokens.py` (tokenizer with NFC normalisation, Bangla→ASCII digit mapping, `Number`/`Multiplier`/`Currency` token types), and full `_parse.py` implementation. Supports Bangla and English digits, lakh/crore/hazar/million/billion multipliers and common spelling variants, grouping commas (lakh and western styles), decimal multipliers (e.g. `2.5 crore`), and currency-marker stripping. 75 tests passing across all four supported Python versions.
- Phase 3 — formatter: full `_format.py` with `script` ∈ {`"bangla"`, `"english"`} and `grouping` ∈ {`"lakh"`, `"western"`, `"none"`}. Lakh grouping uses 2-2-3 chunking from the right. Negative numbers supported. Three Hypothesis roundtrip tests (`parse(format(n)) == n`) now active and passing. 126 tests, 100% branch coverage on `_format.py`.
