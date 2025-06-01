from app.config.paths import INVENTORY_XLS_PATH

import pandas as pd
import logging
from flashtext import KeywordProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def load_keywords():

    try:
        dfs = pd.read_excel(INVENTORY_XLS_PATH, sheet_name=None, header=1)
        all_data = pd.concat(dfs.values(), ignore_index=True)

        dfs = pd.DataFrame(all_data)

        return dfs
    except Exception as e:
        logging.error(f"Error loading keywords: {e}")
        return pd.DataFrame()
def load_master_keywords():
    try:
        df = pd.read_excel(INVENTORY_XLS_PATH, sheet_name=None, header=1)
        all_data = pd.concat(df.values(), ignore_index=True)

        df = pd.DataFrame(all_data)

        df["QtyAvail"] = (df["QtyOnHand"]-df["QtyAllocated"]).clip(lower=0)
        df = filter_master_data(df)
        return df
    except Exception as e:
        logging.error(f"Error loading keywords: {e}")
        return pd.DataFrame()
def filter_master_data(df):
    df = df[df["SellingPrice"] != 0]

    keywords = ["do", "not", "use"]

    df = df[~df["Description"].apply(lambda text: contains_all_keywords(text, keywords))]
    df = df[~df["LongDesc"].apply(lambda text: contains_all_keywords(text, keywords))]
    keywords = ["DISCONTINUED ITEM"]
    df = df[~df["Description"].apply(lambda text: contains_all_keywords(text, keywords))]
    df = df[~df["LongDesc"].apply(lambda text: contains_all_keywords(text, keywords))]
    keywords = ["D O  N O T  U S E"]
    df = df[~df["Description"].apply(lambda text: contains_all_keywords(text, keywords))]
    df = df[~df["LongDesc"].apply(lambda text: contains_all_keywords(text, keywords))]
    return df

def contains_all_keywords(text, keywords):
    keyword_processor = KeywordProcessor(case_sensitive=False)#
    for word in keywords:
        keyword_processor.add_keyword(word, keyword_processor)
    found_keywords = set(keyword_processor.extract_keywords(str(text)))
    return set(keywords).issubset(found_keywords)

if __name__ == "__main__":
    df = load_master_keywords()
    if not df.empty:
        print("Keywords loaded successfully:")
        print(df.head())
    else:
        print("Failed to load keywords.")