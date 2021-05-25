import requests
from bs4 import BeautifulSoup
from google.cloud import firestore


def update_movie_batch(title, db, update_batch):
    # Try to find if movie already exists
    existing_docs = db.collection('movies').where('name', '==', title).get()

    # Create another movie document if doesn't exist
    if len(existing_docs) == 0:
        doc_ref = db.collection('movies').document()
        update_batch.set(doc_ref, {'name': title})
        return 1
    # Or don't do anything (update existing movie document)
    else:
        return 0
    #     doc_ref = existing_docs[0].reference
    #     update_batch.update(doc_ref, {'name': title})


def update_movie_names():
    imdb_websites = [
        'https://www.imdb.com/search/title/?groups=top_1000&start='
    ]

    db = firestore.Client()
    update_batch = db.batch()

    total_entries = 1000
    entries_per_page = 50

    max_batch_updates = 500     # Max allowed by Google Cloud
    num_batch_updates = 0

    for base_website in imdb_websites:
        for start_entry_num in range(1, total_entries, entries_per_page):
            imdb_website = f'{base_website}{start_entry_num}'

            r = requests.get(imdb_website)
            soup = BeautifulSoup(r.content, features='html.parser')

            title_header_elements = soup.find_all('h3', class_='lister-item-header')
            for title_header_element in title_header_elements:
                title = title_header_element.a.get_text()

                num_batch_updates += update_movie_batch(title, db, update_batch)

                if max_batch_updates <= num_batch_updates:
                    update_batch.commit()
                    return

    if num_batch_updates == 0:
        print('No new movie updates from IMDB')

    update_batch.commit()


if __name__ == '__main__':
    update_movie_names()
