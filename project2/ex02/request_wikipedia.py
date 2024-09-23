# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    request_wikipedia.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/23 16:51:17 by josfelip          #+#    #+#              #
#    Updated: 2024/09/23 16:51:20 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests

def fetch_wikipedia_page(page_title):
    url = "https://pt.wikipedia.org/w/api.php"  # Using the Portuguese Wikipedia

    # Parameters for the Wikipedia API request
    params = {
        'action': 'query',
        'format': 'json',
        'titles': page_title,
        'prop': 'extracts',
        'exintro': True,  # Get only the introduction
        'explaintext': True  # Plain text instead of HTML
    }

    # Send the request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        page_id = next(iter(data['query']['pages']))  # Get first (and likely only) page ID

        if page_id == "-1":
            print(f"Page '{page_title}' does not exist.")
            return None  # Return None if page doesn't exist
        else:
            page = data['query']['pages'][page_id]
            return page['title'], page['extract']
    else:
        print(f"Failed to fetch the page. Status Code: {response.status_code}")
        return None

def save_to_file(page_title, content):
    # Format the file name: replace spaces with underscores and add .wiki extension
    file_name = f"{page_title.replace(' ', '_')}.wiki"
    
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Content saved to {file_name}")

def main():
    import sys
    if len(sys.argv) > 1:
        page_title = sys.argv[1]
    else:
        page_title = input("Enter a Wikipedia page title: ")

    result = fetch_wikipedia_page(page_title)

    if result:
        title, extract = result
        save_to_file(title, extract)

if __name__ == "__main__":
    main()
