# Bulbapedia Wiki Scraper

Implementation of bulbapedia wiki scraper featuring multiple commands such as:

## Commands

1. **Summary** — fetches first sentence of given article as it's summary.
2. **Table** — searches and prints out n-th table in the article.
3. **Count-words** — counts words in the article and writes them to `word-count.json`.
4. **Analyze relative word frequency** — uses `Analyzer` to compare frequencies from `word-count.json` with general language frequencies.
5. **Auto count words** — recursively counts words using links.

---

## Usage

Usages respectively (phrase is the last section after `/` in bulbapedias' article link):

python wiki_scraper.py ...

1) Summary
python wiki_scraper.py summary "phrase"

2) Table
python wiki_scraper.py table "phrase" --number n [--first-row-is-header]

3) Count-words
python wiki_scraper.py count-words "phrase"

4) Analyze relative word frequency
python wiki_scraper.py analyze-relative-word-frequency --mode "article/language" --count n [--chart "chart/path.png"]

5) Auto count words
python wiki_scraper.py auto-count-words "start phrase" --depth n --wait t

---

## Notes

This pyhton programe uses custom exceptions and argparse library to detect incorrect usage or/and article problems

---

## Tests & Additional Files

It also contains:

- 5 unit tests - run using pytest in terminal.
- 1 integration test that verifies collaboration between the most important modules, run using python wiki_scraper_integration_test.py.
- Analysis.ipynb which is a notebook file featuring article analisys for multiple languages (deutch, polish, english), function to detect articles language using cosine similarity and coverage of top frequency words from article language and conclusions that I drew after performing the analisys.
