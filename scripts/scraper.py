import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def scrape_goodreads_top_books(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção para erros de HTTP

        soup = BeautifulSoup(response.content, 'html.parser')

        books = []
        rows = soup.find_all('tr')
        print(f"Total de linhas encontradas: {len(rows)}")

        for book in rows:
            title_element = book.find('a', class_='bookTitle')
            author_element = book.find('a', class_='authorName')
            rating_element = book.find('span', class_='minirating')

            if title_element and author_element and rating_element:
                title = title_element.text.strip()
                author = author_element.text.strip()
                rating = rating_element.text.strip()
                print(f"Title: {title.ljust(25)} | Author: {author.ljust(25)} | Rating: {rating}")
                books.append([title, author, rating])

        return books

    except requests.exceptions.HTTPError as err:
        print(f"Erro ao acessar a página: {err}")
        return []

def save_to_csv(books, filename):
    if not books:
        print("Nenhum livro foi encontrado.")
        return

    df = pd.DataFrame(books, columns=['Title', 'Author', 'Rating'])
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"
    books = scrape_goodreads_top_books(url)
    
    if books:
        save_to_csv(books, 'top_books.csv')

        # Carregar os dados do CSV para um DataFrame
        try:
            df = pd.read_csv('top_books.csv')
            print(df.head())

            # Extrair os valores de rating como números float
            df['Rating Value'] = df['Rating'].str.extract(r'(\d\.\d+)').astype(float)

            # Plotar a distribuição das avaliações
            df['Rating Value'].plot(kind='hist', bins=20, title='Distribuição de Avaliações')
            plt.xlabel('Rating')
            plt.ylabel('Frequency')
            plt.show()

        except FileNotFoundError:
            print("O arquivo CSV não foi encontrado.")

    else:
        print("Nenhum livro encontrado durante o scraping.")
