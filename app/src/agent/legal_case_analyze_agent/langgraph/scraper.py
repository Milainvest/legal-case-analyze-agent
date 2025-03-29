"""
Contains functions for scraping case text from web sources.
"""
import requests
from bs4 import BeautifulSoup
import time

def scrape_case_text(url: str) -> str | None:
    """
    Attempts to scrape the main case text from a given URL.

    Args:
        url: The URL of the case page.

    Returns:
        The extracted case text as a string, or None if scraping fails.
    """
    print(f"--- Attempting to scrape: {url} ---")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # Basic request with timeout and headers
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Basic parsing with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Parsing Logic ---
        # TODO: Add parsers for other potential sources.
        # TODO: Improve robustness (handle variations in HTML, CAPTCHAs, blocks).

        text_content = None

        # Implementation for Justia (supreme.justia.com)
        if "supreme.justia.com" in url:
            print("--- Applying Justia parsing logic ---")
            # Justia often has the main opinion within <div id="opinion">
            # Or sometimes within divs having specific data attributes or classes.
            opinion_div = soup.find('div', id='opinion')

            # Fallback selectors if id="opinion" isn't found
            if not opinion_div:
                # Look for common text block classes/structures
                possible_containers = soup.find_all('div', class_=lambda x: x and 'text-block' in x)
                if possible_containers:
                    # Assume the largest text block is the opinion (heuristic)
                    opinion_div = max(possible_containers, key=lambda div: len(div.get_text()))
                else:
                    # Last resort: find main content area if available
                    main_content = soup.find('main') or soup.find('article') or soup.body
                    if main_content:
                       opinion_div = main_content # Search within main if specific div fails

            if opinion_div:
                # Attempt to remove known clutter like headers, footers, related content links within the div
                for clutter_selector in ['header', 'footer', '.related-content', '.noprint', '.annotations']:
                    for element in opinion_div.select(clutter_selector):
                        element.decompose() # Remove the element and its content

                # Extract text, joining paragraphs for better structure
                paragraphs = opinion_div.find_all('p')
                if paragraphs:
                    # Filter out short paragraphs that might be headers/footers missed by selectors
                    text_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True) and len(p.get_text(strip=True)) > 50) # Heuristic: ignore very short paragraphs
                    print(f"--- Scrape successful: Extracted content from Justia using <p> tags ---")
                    # Add debug logging for text content
                    print(f"--- Scraped text preview: {text_content[:200]}... ---")
                    print(f"--- Total text length: {len(text_content)} characters ---")
                    # Add debug logging for first few paragraphs
                    first_paragraphs = text_content.split('\n\n')[:3]
                    for i, p in enumerate(first_paragraphs):
                        print(f"--- Paragraph {i+1} preview: {p[:200]}... ---")
                else:
                    # Fallback to getting all text if no <p> tags found within container
                    text_content = opinion_div.get_text(separator='\n', strip=True)
                    if text_content:
                         print(f"--- Scrape successful: Extracted content from Justia using fallback get_text ---")
                         # Add debug logging for text content
                         print(f"--- Scraped text preview: {text_content[:200]}... ---")
                         print(f"--- Total text length: {len(text_content)} characters ---")
                         # Add debug logging for first few paragraphs
                         first_paragraphs = text_content.split('\n')[:3]
                         for i, p in enumerate(first_paragraphs):
                             print(f"--- Paragraph {i+1} preview: {p[:200]}... ---")
                    else:
                         print("--- Scrape warning: Found opinion div but no text extracted (Justia) ---")
                         text_content = None # Reset if empty
            else:
                print("--- Scrape failed: Could not find suitable opinion container (Justia) ---")

        # Example for CourtListener (structure might change!)
        elif "courtlistener.com/opinion" in url:
            print("--- Applying CourtListener parsing logic ---")
            # CourtListener often uses <div id="opinion-content"> or similar
            opinion_div = soup.find('div', id='opinion-content')
            # Sometimes content might be within specific classes like 'content' inside 'article'
            if not opinion_div:
                 article_content = soup.find('article', class_='content')
                 if article_content:
                     opinion_div = article_content

            if opinion_div:
                 # Remove clutter (e.g., citation links, headers)
                 for clutter_selector in ['.hide-small', '.page-header', 'script', 'style', '.noprint']:
                     for element in opinion_div.select(clutter_selector):
                         element.decompose()

                 # Extract text, joining paragraphs
                 paragraphs = opinion_div.find_all('p')
                 if paragraphs:
                     text_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                     print(f"--- Scrape successful: Extracted content from CourtListener using <p> tags ---")
                 else:
                     text_content = opinion_div.get_text(separator='\n', strip=True)
                     if text_content:
                          print(f"--- Scrape successful: Extracted content from CourtListener using fallback get_text ---")
                     else:
                          print("--- Scrape warning: Found opinion div but no text extracted (CourtListener) ---")
                          text_content = None
            else:
                 print("--- Scrape failed: Could not find suitable opinion container (CourtListener) ---")


        # Add more site-specific parsers here using elif
        # elif "another-site.com" in url:
        #     print("--- Applying AnotherSite parsing logic ---")
        #     # ... parsing logic ...

        # Final check and return
        if text_content:
            return text_content.strip() # Return cleaned text
        else:
            # Log failure if no content was extracted
            print(f"--- Scrape failed: No content extracted from {url} ---")
            return None

    except requests.exceptions.RequestException as e:
        print(f"--- Scrape failed: Request error - {e} ---")
        return None
    except Exception as e:
        print(f"--- Scrape failed: Parsing or other error - {e} ---")
        return None

    # Add a small delay to be polite to the server
    time.sleep(1)
