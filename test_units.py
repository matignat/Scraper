"""
Unit tests for wiki scraper (offline).
These tests verify selected functions/methods without any network access.
Uses pytest
"""

from pathlib import Path
import pytest
import json
import scraper_logic
from scraper_logic import Scraper
from argparser_logic import arg_parser
from freq_analyzer import WikiAnalyzer

# We use pytest that gives us tmp_path and cleans after test
def write_html(tmp_path: Path, html: str, name: str = "page.html") -> Path:
    """Saves html into file and returns path"""
    p = tmp_path / name
    p.write_text(html, encoding="utf-8")
    return p


def test_get_source(tmp_path):
    # Tests get_source() scraper method
    html = """
    <html><body>
      <div id="mw-content-text">
        <p> Serious things here. </p>
      </div>
    </body></html>
    """
    html_path = write_html(tmp_path, html)

    s = Scraper("Nothing important", local_html_path=str(html_path))
    content = s.get_source()

    assert content is not None
    assert content.name == "div"
    assert content.get("id") == "mw-content-text"
    assert "Serious things here." in content.get_text(" ", strip=True)

def test_count_words(tmp_path, monkeypatch):
    # Tests only: Scraper.count_words()
    html = """
    <html><body>
    <div id="mw-content-text">
        <p> uwielbiam Mim mim2 MIM _mim_ </p>
    </div>
    </body></html>
    """
    html_path = write_html(tmp_path, html)

    # Monkeypatch file atr. from scraper to use path from pytest
    fake_module_file = tmp_path / "fake_scraper_logic.py"
    monkeypatch.setattr(scraper_logic, "__file__", str(fake_module_file))

    s = Scraper("Python jest super", local_html_path=str(html_path))
    s.count_words()

    json_path = tmp_path / "word-counts.json"
    assert json_path.exists()

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["mim"] == 4
    assert data["uwielbiam"] == 1

def test_scraper_init():
    s = Scraper("Team Rocket")
    assert s.phrase == "Team_Rocket"


def test_arg_parser():
    args = arg_parser(["table", "Team Rocket", "--number", "2", "--first-row-is-header"])

    assert args.command == "table"
    assert args.phrase == "Team Rocket"
    assert args.number == 2
    assert args.first_row_is_header is True


def test_make_summary(tmp_path):
    html = """
    <html><body>
      <div id="mw-content-text">
        <p> Ten zwracamy :) </p>
        <p> A ten nie :( </p>
      </div>
    </body></html>
    """
    html_path = write_html(tmp_path, html)

    s = Scraper("Testy teściki", local_html_path=str(html_path))
    summary = s.make_summary()

    assert summary == "Ten zwracamy:)"
