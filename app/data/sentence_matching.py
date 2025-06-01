import pandas as pd
from flashtext import KeywordProcessor
from app.utils.load_keywords import load_keywords, load_master_keywords

keyword_processor = KeywordProcessor(case_sensitive=False)
passkey_processor = KeywordProcessor(case_sensitive=True)
keyword_processor_2 = KeywordProcessor(case_sensitive=False)

keywords = ["crs"]
def build_flashtext_processor(df):
    for code in df['StockCode'].dropna().unique():
        keyword_processor.add_keyword(code)
    for code in df['AlternateKey1'].dropna().unique():
        keyword_processor.add_keyword(code)
    for code in df['AlternateKey2'].dropna().unique():
        keyword_processor.add_keyword(code)

def build_passkeys_processor():
    passkey_processor.add_keywords_from_list(keywords)

def warehouse_conversion(num):
    if num == 1:
        return "Langley"
    if num == 6:
        return "Burnaby"
    if num == 8:
        return "Kelowna"
    return "Unknown Warehouse"


def get_stock_info(df, matched_letters, matched_keypass):


    result = df[df['StockCode'] == matched_letters]
    if result.empty: #and "crs" in matched_keypass:
        result = df[df['AlternateKey1'] == matched_letters]

    if result.empty: # and "crs" in matched_keypass:
        result = df[df['AlternateKey2'] == matched_letters]

    if not result.empty:
        row = result.iloc[0]
        warehouse_string = ""
        for x in range(len(result)):
            warehouse_string += f"{warehouse_conversion(result.iloc[x].get('Warehouse', 'N/A'))} Quantity: {max(0, result.iloc[x].get('QtyAvail', 'N/A'))}\n"
        url_string = f"https://wescovan.com/search?search_api_views_fulltext={row['StockCode']}"
            #hyperlink = f"\033]8;;{url_string}\033\\{row['StockCode']}\033]8;;\033\\"
        hyperlink = f"{url_string}"
        return_string = (f"Stock #: {row['StockCode']}\n"
                             f"{row['Description']}\n"
                             f"{row.get('LongDesc', 'N/A')}\n"
                             f"Mfg Stock #: {row.get('AlternateKey1', 'N/A')}\n"
                             f"{warehouse_string}\n"
                             f"Price: ${row['SellingPrice']}/{row['StockUom']}\n"
                             f"Weight(lbs.): {row['Mass']}/{row['StockUom']}\n"
                             f"\n"
                             f"Website: {hyperlink}\n"
                             f"\n"

                             f"Please be sure to call branch to confirm quantity is available.\n"
                             f"Langley Tel: 604.881.3000\n"
                             f"Burnaby Tel: 604.292.1220\n"
                             f"Kelowna Tel: 604.491.1055"
                             )
        if pd.isna(row.get('AlternateKey1', 'N/A')):
            return_string = (f"Stock #: {row['StockCode']}\n"
                             f"{row['Description']}\n"
                             f"{row.get('LongDesc', 'N/A')}\n"
                             f"{warehouse_string}\n"
                             f"Price: ${row['SellingPrice']}/{row['StockUom']}\n"
                             f"Weight(lbs.): {row['Mass']}/{row['StockUom']}\n"
                             f"\n"
                             f"Website: {hyperlink}\n"
                             f"\n"

                             f"Please be sure to call branch to confirm quantity is available.\n"
                             f"Langley Tel: 604.881.3000\n"
                             f"Burnaby Tel: 604.292.1220\n"
                             f"Kelowna Tel: 604.491.1055"
                             )

            return_string = return_string_creation(result)

        return return_string

    return "Stock code not found. Try again."
def is_valid(value, exclude_strings={"N/A"}):
    return pd.notna(value) and value not in exclude_strings

def return_string_creation(result):
    warehouse_string = ""
    for x in range(len(result)):
        warehouse_string += f"{warehouse_conversion(result.iloc[x].get('Warehouse', 'N/A'))} Quantity: {int(max(0, result.iloc[x].get('QtyAvail', 'N/A')))}\n"
    row = result.iloc[0]
    return_string = ""
    if is_valid(row["StockCode"]):
        return_string += "Stock #: " + row["StockCode"] + "\n"

    if is_valid(row["Description"]):
        return_string += row["Description"] + "\n"

    if is_valid(row.get("LongDesc", "N/A")):
        return_string += row["LongDesc"] + "\n"

    if is_valid(row.get("AlternateKey1", "N/A")):
        return_string += "Mfg Stock #: " + row["AlternateKey1"] + "\n"

    if is_valid(warehouse_string):
        return_string += warehouse_string + "\n"

    if is_valid(row["SellingPrice"]) and is_valid(row["StockUom"]):
        return_string += "Price: $" + str(row["SellingPrice"]) + "/" + row["StockUom"] + "\n"

    if is_valid(row["Mass"]) and is_valid(row["StockUom"]):
        return_string += "Weight(lbs.): " + str(row["Mass"]) + "/" + row["StockUom"] + "\n"

    url_string = f"https://wescovan.com/search?search_api_views_fulltext={row['StockCode']}"

    hyperlink = f"{url_string}"

    return_string += (f"\n"f"Website: {hyperlink}\n"
                             f"\n"

                             f"Please be sure to call branch to confirm quantity is available.\n"
                             f"Langley Tel: 604.881.3000\n"
                             f"Burnaby Tel: 604.292.1220\n"
                             f"Kelowna Tel: 604.491.1055")
    return return_string

def stock_matching(user_input):
    df = load_master_keywords()
    if not df.empty:
        build_flashtext_processor(df)
        build_passkeys_processor()

        matched_code = keyword_processor.extract_keywords(user_input)
        matched_keypass = passkey_processor.extract_keywords(user_input)

        if matched_code:
            response = get_stock_info(df, matched_code[0], matched_keypass)

        else:
            return None
            response = "Hello, an operator will response when available"


        return response
    else:
        print("Failed to load stock data.")
        return None


if __name__ == "__main__":
    user_input = input("Enter stock code: ")

    print(stock_matching(user_input))
#how 84TRN-JJ3224CR and 84TRN-JJ4012CR

