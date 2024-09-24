# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    roads_to_philosophy.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/24 12:44:12 by josfelip          #+#    #+#              #
#    Updated: 2024/09/24 12:44:15 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
from bs4 import BeautifulSoup
import time
import sys

# Wikipedia base URL
WIKI_BASE_URL = "https://en.wikipedia.org"

def validate_article_url(query):
    """Validates if the direct Wikipedia URL for the given query exists."""
    article_url = f"{WIKI_BASE_URL}/wiki/{query.replace(' ', '_')}"
    response = requests.get(article_url)
    
    if response.status_code == 200:
        return article_url
    else:
        print(f"No valid article found for '{query}'")
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
    titles = []

    while current_url:
        if current_url in visited:
            print("Detected a loop! Exiting...")
            return steps

        visited.add(current_url)

        # Get the title of the current page
        response = requests.get(current_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text
            titles.append(title)
        else:
            print(f"Failed to retrieve the page at {current_url}.")
            break

        print(f"Step {steps}: {title}")

        if "Philosophy" in title:
            print(f"Reached the Philosophy page in {steps} steps!")
            return steps, titles

        first_link = get_first_link(current_url)
        if not first_link:
            print("No further links found. Stopping.")
            break

        current_url = first_link
        steps += 1

        # Pause between requests to avoid overwhelming Wikipedia's servers
        time.sleep(0.5)

    return steps, titles

def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("Enter a Wikipedia search term: ")

    start_url = validate_article_url(query)
    if start_url:
        steps, titles = trace_to_philosophy(start_url)
        print("\n".join(titles))
        print(f"\n{steps} roads from {query} to philosophy!")

if __name__ == "__main__":
    main()
