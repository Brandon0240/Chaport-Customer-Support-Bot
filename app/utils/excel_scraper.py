
import os
from app.config.paths import SCRAPED_DATA_DIR
from app.utils.load_keywords import load_master_keywords
from app.data.sentence_matching import stock_matching

def create_sheet(name):
    df = load_master_keywords()
    filename = os.path.join(SCRAPED_DATA_DIR, name)
    dirpath = os.path.dirname(filename)
    os.makedirs(dirpath, exist_ok=True)
    with open(filename, "a", encoding="utf-8") as file:
        for code in df['StockCode'].dropna().unique():
            print(code)
            file.write(f"{stock_matching(code)}\n")
            file.write(f"{'='*80}\n")

if __name__ == "__main__":
    create_sheet("test_website_data.txt")
