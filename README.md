# doshomik

[![CI](https://github.com/rayhan-mahmuud/doshomik/actions/workflows/ci.yml/badge.svg)](https://github.com/rayhan-mahmuud/doshomik/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/doshomik.svg)](https://pypi.org/project/doshomik/)
[![Python versions](https://img.shields.io/pypi/pyversions/doshomik.svg)](https://pypi.org/project/doshomik/)
[![License: MIT](https://img.shields.io/github/license/rayhan-mahmuud/doshomik.svg)](https://github.com/rayhan-mahmuud/doshomik/blob/master/LICENSE)

Parse and format South Asian numeric strings — Bangla and English digits, lakh-crore system, currency markers.

```python
from doshomik import parse, format

parse("১ কোটি ২৫ লক্ষ")   # → 12_500_000
parse("2.5 crore")          # → 25_000_000
parse("৳ 1,25,000")         # → 125_000

format(12_500_000, script="bangla",   grouping="lakh")    # → "১,২৫,০০,০০০"
format(12_500_000, script="english",  grouping="lakh")    # → "1,25,00,000"
format(12_500_000, script="english",  grouping="western") # → "12,500,000"
```

## Installation

### pip

```bash
pip install doshomik
```

### uv

```bash
uv add doshomik
```

Requires Python 3.10 or later. No runtime dependencies.

## Usage

### Parsing

`parse(s)` accepts a string containing South Asian numeric notation and returns a plain `int`.

```python
from doshomik import parse

# Bangla digits
parse("১২৩")           # → 123
parse("০")             # → 0

# English digits
parse("125000")        # → 125_000

# Multiplier words (Bangla and English)
parse("১ হাজার")       # → 1_000
parse("1 hazar")       # → 1_000
parse("1 thousand")    # → 1_000

parse("১ লাখ")         # → 100_000
parse("1 lakh")        # → 100_000
parse("1 lac")         # → 100_000

parse("১ কোটি")        # → 10_000_000
parse("1 crore")       # → 10_000_000

# Compound expressions
parse("১ কোটি ২৫ লক্ষ")         # → 12_500_000
parse("1 crore 25 lakh")         # → 12_500_000
parse("1 crore 50 lakh 25 hazar") # → 15_025_000

# Decimal multipliers
parse("2.5 crore")    # → 25_000_000
parse("1.5 lakh")     # → 150_000

# Grouped numbers (lakh and western styles)
parse("1,25,000")     # → 125_000
parse("1,000,000")    # → 1_000_000

# Currency markers are stripped automatically
parse("৳ 1,25,000")   # → 125_000
parse("500 taka")     # → 500
parse("500 tk.")      # → 500
parse("bdt 250")      # → 250

# International (as used in English-language BD press)
parse("1 million")    # → 1_000_000
parse("1 billion")    # → 1_000_000_000

# Mixed script
parse("১০ lakh")      # → 1_000_000
parse("10 লাখ")       # → 1_000_000
```

**What `parse` accepts:**

| Category | Examples |
|---|---|
| Bangla digits | `০১২৩৪৫৬৭৮৯` |
| English digits | `0123456789` |
| Thousands | `hazar`, `hajar`, `thousand`, `k`, `হাজার` |
| Lakhs | `lakh`, `lac`, `lakhs`, `লাখ`, `লক্ষ` |
| Crores | `crore`, `crores`, `cr`, `কোটি` |
| International | `million`, `mn`, `m`, `billion`, `bn`, `b` |
| Grouping commas | lakh-style (`1,25,000`) and western (`1,000,000`) |
| Currency markers | `৳`, `tk`, `tk.`, `taka`, `টাকা`, `rs`, `rs.`, `bdt` |
| Decimal multipliers | `2.5 crore`, `1.5 lakh` |

**What `parse` does NOT accept:**

- Bare decimals without a multiplier (`"1.5"` raises `ParseError` — result is not an integer)
- Strings with no numeric content (`"abc"`, `""`)
- Standalone multipliers (`"crore"`, `"লাখ"`)

### Formatting

`format(n, *, script, grouping)` converts a plain `int` to a formatted string.

```python
from doshomik import format

# script="bangla" | "english"
# grouping="lakh"  | "western" | "none"

format(125_000, script="english", grouping="lakh")    # → "1,25,000"
format(125_000, script="bangla",  grouping="lakh")    # → "১,২৫,০০০"
format(125_000, script="english", grouping="western") # → "125,000"
format(125_000, script="bangla",  grouping="western") # → "১২৫,০০০"
format(125_000, script="english", grouping="none")    # → "125000"
format(125_000, script="bangla",  grouping="none")    # → "১২৫০০০"

# Negative numbers
format(-1_000_000, script="english", grouping="lakh")    # → "-10,00,000"
format(-1_000_000, script="bangla",  grouping="lakh")    # → "-১০,০০,০০০"
```

**Lakh grouping** follows the South Asian convention: the rightmost group has 3 digits, every group to the left has 2 digits.

```
12,50,00,000  →  "12 crore 50 lakh"
 1,25,000     →  "1 lakh 25 thousand"
```

**Default arguments:** `script="bangla"`, `grouping="lakh"` — i.e., `format(n)` produces a Bangla-script lakh-grouped string.

### Error handling

```python
from doshomik import parse, format
from doshomik import ParseError, FormatError, DoshomikError

# DoshomikError is the base class for both ParseError and FormatError
try:
    value = parse("not a number")
except ParseError as e:
    print(e)  # no numeric content found in 'not a number'

try:
    result = format(1.5, script="english", grouping="lakh")
except FormatError as e:
    print(e)  # n must be int, got float

# Catch either with the base class
try:
    parse("crore")  # multiplier without preceding number
except DoshomikError as e:
    print(type(e).__name__, e)
```

**`ParseError` is raised when:**

- The input contains no numeric content
- A multiplier appears without a preceding number
- The computed result is not a whole integer (e.g. `"1.5"` with no multiplier)

**`FormatError` is raised when:**

- `n` is not a plain `int` (floats, strings, `None`, and `bool` are all rejected)
- `script` is not `"bangla"` or `"english"` (case-sensitive)
- `grouping` is not `"lakh"`, `"western"`, or `"none"` (case-sensitive)

## API reference

### `parse(s: str) -> int`

Parse a South Asian numeric string and return an integer.

| Parameter | Type | Description |
|---|---|---|
| `s` | `str` | Input string to parse |

Raises `ParseError` on invalid input.

### `format(n: int, *, script: str = "bangla", grouping: str = "lakh") -> str`

Format an integer as a South Asian numeric string.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n` | `int` | — | Integer to format (booleans rejected) |
| `script` | `str` | `"bangla"` | `"bangla"` or `"english"` |
| `grouping` | `str` | `"lakh"` | `"lakh"`, `"western"`, or `"none"` |

Raises `FormatError` on invalid arguments.

### Exceptions

| Exception | Base | When |
|---|---|---|
| `DoshomikError` | `Exception` | Base class |
| `ParseError` | `DoshomikError` | Input cannot be parsed |
| `FormatError` | `DoshomikError` | Arguments are invalid |

## Contributing

```bash
git clone https://github.com/rayhan-mahmuud/doshomik
cd doshomik
uv sync --all-groups

# Run the full test suite (pytest + coverage)
uv run pytest

# Type check
uv run mypy

# Lint and format
uv run ruff check src tests
uv run ruff format src tests
```

Tests target Python 3.10–3.13. Property-based tests use [Hypothesis](https://hypothesis.readthedocs.io/).

## Changelog

See [CHANGELOG.md](https://github.com/rayhan-mahmuud/doshomik/blob/master/CHANGELOG.md).

## License

MIT — see [LICENSE](https://github.com/rayhan-mahmuud/doshomik/blob/master/LICENSE).
