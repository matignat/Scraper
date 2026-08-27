# Bulbapedia Wiki Scraper

A Python web scraper for [Bulbapedia](https://bulbapedia.bulbagarden.net/) that allows users to retrieve article summaries, extract tables, analyze word frequencies, and recursively explore linked articles.

The project was built to practice web scraping, HTML parsing, command-line interfaces, automated testing, and basic text analysis.

## Features

* **Summary** — retrieves the first sentence of a given Bulbapedia article.
* **Table** — extracts and displays a selected table from an article.
* **Count words** — counts word occurrences in an article and saves the results to `word-count.json`.
* **Relative word frequency analysis** — compares article word frequencies with general language frequency data and can generate a chart.
* **Auto count words** — recursively follows links between Bulbapedia articles and aggregates word frequencies up to a specified depth.
* **Error handling** — uses custom exceptions to handle invalid commands, invalid arguments, and article-related errors.
* **CLI** — uses `argparse` to provide a command-line interface.

## Technologies

* Python 3
* `requests` — HTTP requests
* `BeautifulSoup` — HTML parsing
* `argparse` — command-line interface
* `pytest` — unit testing
* `matplotlib` — data visualization
* Jupyter Notebook — exploratory data analysis

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/matignat/Scraper
cd https://github.com/matignat/Scraper

pip install -r requirements.txt
```

## Usage

The article identifier is the final part of a Bulbapedia article URL.

### 1. Summary

Returns the first sentence of an article.

```bash
python wiki_scraper.py summary "Pikachu"
```

### 2. Table

Extracts the `n`-th table from an article.

```bash
python wiki_scraper.py table "Pikachu" --number 2
```

To treat the first row as a table header:

```bash
python wiki_scraper.py table "Pikachu" --number 2 --first-row-is-header
```

### 3. Count words

Counts the words occurring in an article and saves the results to `word-count.json`.

```bash
python wiki_scraper.py count-words "Pikachu"
```

### 4. Analyze relative word frequency

Compares word frequencies from `word-count.json` with general language frequencies.

```bash
python wiki_scraper.py analyze-relative-word-frequency --mode article --count 20
```

A chart can optionally be generated:

```bash
python wiki_scraper.py analyze-relative-word-frequency \
    --mode article \
    --count 20 \
    --chart "charts/frequency.png"
```

### 5. Auto count words

Recursively follows links from a starting article and counts words across the visited articles.

```bash
python wiki_scraper.py auto-count-words "Pikachu" --depth 2 --wait 1
```

* `--depth` controls how many levels of links are followed.
* `--wait` specifies the delay between requests.


## Testing

The project contains **5 unit tests** covering individual components and **1 integration test** checking the cooperation between the main modules.

Run the unit tests with:

```bash
pytest
```

Run the integration test with:

```bash
python wiki_scraper_integration_test.py
```

## Data Analysis

`Analysis.ipynb` contains additional experiments performed on the collected word-frequency data.

The notebook includes:

* analysis of articles in **English, Polish, and German**,
* comparison of word-frequency distributions,
* language detection using **cosine similarity**,
* analysis of the coverage provided by the most frequent words in each language,
* conclusions based on the collected data.
