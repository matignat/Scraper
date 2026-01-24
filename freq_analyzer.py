import json
import pandas as pd
import matplotlib.pyplot as plt
from wordfreq import get_frequency_dict
from pathlib import Path

class WikiAnalyzer:
    def __init__(self, json_path="./word-counts.json", lang="en"):
        self.json_path = json_path
        self.lang = lang
        self.article_data = self._load_article_data()
        self.language_data = self._load_language_data()

    def _load_article_data(self):
        """Loads word-count.json file or empty dict if file does"t exist"""
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def _load_language_data(self): 
        """Loads frequencies from dictionary in wiki language"""
        return get_frequency_dict(self.lang)

    def analyze_frequency(self, mode, count, chart_path=None):
        # Makes 2 column structure with custom names from dicts
        df_wiki = pd.DataFrame(self.article_data.items(), columns=["word", "wiki_freq"])
        df_lang = pd.DataFrame(self.language_data.items(), columns=["word", "lang_freq"])
        
        # Normalize 
        if not df_wiki.empty:
            df_wiki["wiki_freq"] = df_wiki["wiki_freq"] / df_wiki["wiki_freq"].max()

        if not df_lang.empty:
            df_lang["lang_freq"] = df_lang["lang_freq"] / df_lang["lang_freq"].max()

        # Merge statistics together (outer join leaves NaN)
        merged = pd.merge(df_wiki, df_lang, on="word", how="outer")
        merged.columns = ["word", "Frequency in the article", "Frequency in the language"]

        if mode == "article":
            result = merged.sort_values(by="Frequency in the article", ascending=False).head(count)
        else:
            result = merged.sort_values(by="Frequency in the language", ascending=False).head(count)

        print(result.to_string(index=False))

        if chart_path:
            self._generate_chart(result, chart_path, count)

    def _generate_chart(self, df, path, n):
        """Generates chart on given path for count words"""
        width = max(10, n * 0.8)
        
        # Overwrite old charts
        chart_path = Path(path)
        chart_path.parent.mkdir(parents=True, exist_ok=True)

        cols = ["Frequency in the article", "Frequency in the language"]

        # Change NaN to 0 after outer join
        df[cols] = df[cols].fillna(0)

        df.plot(kind="bar", x="word", y=cols, figsize=(width, 6))
        
        plt.xticks(rotation=45)
        plt.title("Frequency of words in the article vs in the language") 
        plt.legend(["Article", "Language"]) 
        plt.ylabel("Normalized Frequency")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()