"""
Defines the list of known cases for automatic retrieval attempt.
Maps case names (or identifiers) to potential source URLs for scraping.
"""

# NOTE: Use consistent identifiers (e.g., lowercase, no spaces) if matching input caseName

KNOWN_CASES_SOURCES = {
    "marbury v. madison": "https://supreme.justia.com/cases/federal/us/5/137/", # Example URL
    "mcculloch v. maryland": "https://supreme.justia.com/cases/federal/us/17/316/", # Example URL
    # Add ~20-30 more common US law cases here
    # ...
    "placeholder_case_1": "http://example.com/placeholder1",
    "placeholder_case_2": "http://example.com/placeholder2",
}

def get_known_case_url(case_name: str) -> str | None:
    """
    Checks if the case name matches a known case and returns its source URL.
    Performs simple case-insensitive matching for now.
    """
    normalized_case_name = case_name.lower().strip()
    return KNOWN_CASES_SOURCES.get(normalized_case_name)
