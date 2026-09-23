# Books Scraper

Projet Scrapy pour scraper le site books.toscrape.com et récupérer les infos de tous les livres (titre, prix, note, stock, catégorie, description...).

## Installation

```
pip install -r requirements.txt
```

## Lancer le spider

```
scrapy crawl books
```

## Export

```
scrapy crawl books -O books.csv
```

```
scrapy crawl books -O books.json
```

## Structure

- `books_scraper/spiders/books.py` : le spider, il scrape le catalogue, suit chaque livre pour avoir le détail, et gère la pagination automatiquement
- `books_scraper/items.py` : les champs du BookItem
- `books.csv` : le résultat final