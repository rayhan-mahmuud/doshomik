BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"
ENGLISH_DIGITS = "0123456789"

# bangla digit → ascii digit
DIGIT_MAP = {bn: en for bn, en in zip(BANGLA_DIGITS, ENGLISH_DIGITS, strict=True)}

# multiplier words → multiplier value
# includes common spelling variants and both scripts
MULTIPLIERS = {
    # thousands
    "hazar": 1_000,
    "hajar": 1_000,
    "thousand": 1_000,
    "k": 1_000,
    "হাজার": 1_000,
    # lakhs (100,000)
    "lakh": 100_000,
    "lac": 100_000,
    "lakhs": 100_000,
    "লাখ": 100_000,
    "লক্ষ": 100_000,
    "লক্ষ্য": 100_000,  # common misspelling
    # crores (10,000,000)
    "crore": 10_000_000,
    "crores": 10_000_000,
    "cr": 10_000_000,
    "কোটি": 10_000_000,
    # millions / billions — sometimes appear in English BD press
    "million": 1_000_000,
    "mn": 1_000_000,
    "m": 1_000_000,
    "billion": 1_000_000_000,
    "bn": 1_000_000_000,
    "b": 1_000_000_000,
}

# tokens to strip or treat as whitespace — currency markers, "taka", etc.
CURRENCY_MARKERS = {"৳", "tk", "tk.", "taka", "টাকা", "rs", "rs.", "bdt"}
