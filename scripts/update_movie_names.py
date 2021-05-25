import requests
from bs4 import BeautifulSoup


def update_movie_names():
    imdb_websites = [
        'https://www.imdb.com/search/title/?groups=top_1000&start='
    ]

    total_entries = 1000
    entries_per_page = 50

    for base_website in imdb_websites:
        for start_entry_num in range(1, total_entries, entries_per_page):
            imdb_website = f'{base_website}{start_entry_num}'

            r = requests.get(imdb_website)
            soup = BeautifulSoup(r.content, features='html.parser')

            title_header_elements = soup.find_all('h3', class_='lister-item-header')
            for title_header_element in title_header_elements:
                title = title_header_element.a.get_text()
                print(title)


if __name__ == '__main__':
    update_movie_names()
