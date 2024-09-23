import requests
from bs4 import BeautifulSoup
import time
import sys

# Wikipedia base URL
WIKI_BASE_URL = "https://en.wikipedia.org"

def perform_search(query):
    """Performs a search on Wikipedia and returns the first article URL."""
    search_url = f"{WIKI_BASE_URL}/w/index.php?search={query.replace(' ', '+')}"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        print(f"Failed to perform search. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Try to find the first article link in the search result
    search_result = soup.find('div', class_='mw-search-result-heading')
    if search_result:
        first_link = search_result.find('a')
        if first_link and first_link.get('href'):
            return WIKI_BASE_URL + first_link['href']
    
    print(f"No valid search result found for '{query}'")
    return None

def get_first_link(url):
    """Fetches the first valid Wikipedia article link from a page."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main content area where the actual article text is located
    content = soup.find(id='mw-content-text')

    if content is None:
        return None

    # Find all paragraphs in the content area
    paragraphs = content.find_all('p', recursive=True)
    
    # Iterate through all paragraphs to find the first valid link
    for para in paragraphs:
        link = para.find('a', recursive=True)
        if link and link.get('href').startswith('/wiki/'):
            # Ensure that the link is not in parentheses and is a valid article link
            href = link.get('href')
            if not href.startswith('/wiki/Help:') and not href.startswith('/wiki/File:') and not href.startswith('/wiki/Special:'):
                return WIKI_BASE_URL + href

    return None

def trace_to_philosophy(start_url):
    """Traces the first link from a given Wikipedia page to the Philosophy page."""
    visited = set()
    current_url = start_url
    steps = 0

    while current_url:
        if current_url in visited:
            print("Detected a loop! Exiting...")
            return steps

        visited.add(current_url)
        print(f"Step {steps}: {current_url}")

        if "Philosophy" in current_url:
            print(f"Reached the Philosophy page in {steps} steps!")
            return steps

        first_link = get_first_link(current_url)
        if not first_link:
            print("No further links found. Stopping.")
            return steps

        current_url = first_link
        steps += 1

        # Pause between requests to avoid overwhelming Wikipedia's servers
        time.sleep(0.5)

    return steps

def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("Enter a Wikipedia search term: ")

    start_url = perform_search(query)
    if start_url:
        trace_to_philosophy(start_url)

if __name__ == "__main__":
    main()
