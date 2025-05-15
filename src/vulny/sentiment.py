# ===== NLTK setup ===== #

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def test():
    from pathlib import Path
    import json
    analysed = []
    with Path("test_data.json").open(mode="rt") as f:
        data = json.loads(f.read())
        for advisory in data:
            content = "\n".join(advisory["_enrichment"])
            ss = sid.polarity_scores(content)
            print(advisory["cve_id"], ":", ss["compound"])
            print()
            advisory["_sentiment"] = ss["compound"]
            analysed.append(advisory)
    with Path("test_data.json").open(mode="wt") as f:
        f.write(json.dumps(analysed, indent=2, ensure_ascii=False))
    
if __name__ == "__main__":
    test()