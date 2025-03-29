"""
Defines the list of known cases for automatic retrieval attempt.
Maps case names (or identifiers) to potential source URLs for scraping.
"""

# NOTE: Use consistent identifiers (e.g., lowercase, no spaces) if matching input caseName
# NOTE: Consider using more stable/scraper-friendly sources like CourtListener where possible.

KNOWN_CASES_SOURCES = {
    # Example Justia URLs (Scraping can be fragile)
    "marbury v. madison": "https://supreme.justia.com/cases/federal/us/5/137/",
    "mcculloch v. maryland": "https://supreme.justia.com/cases/federal/us/17/316/",
    # Add ~20-30 more common US law cases here
    # Example CourtListener URL:
    # "marbury v. madison": "https://www.courtlistener.com/opinion/105339/marbury-v-madison/",
    # ...
    "placeholder_case_1": "http://example.com/placeholder1", # Placeholder
    "placeholder_case_2": "http://example.com/placeholder2", # Placeholder
}

def get_known_case_url(case_name: str) -> str | None:
    """
    Checks if the case name matches a known case and returns its source URL.
    Performs simple case-insensitive matching for now.
    """
    normalized_case_name = case_name.lower().strip()
    return KNOWN_CASES_SOURCES.get(normalized_case_name)
