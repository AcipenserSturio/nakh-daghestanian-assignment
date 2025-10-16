import requests
import pandas as pd


def read_dataframe() -> pd.DataFrame:
    URL = "https://raw.githubusercontent.com/laamxo/dosham/refs/heads/main/unified.json"
    columns = [
        "id",  # unique id, numeric, sparse, obligatory
        "word",  # spelling in cyrillic. includes diacritics, word forms
        "word1",  # spelling stripped of diacritics. nullable
        "translate",  # definition. html. \r\n-terminated
        "parent",  # citation tag?
    ]
    df = []
    for row in requests.get(URL).json():
        df.append([row[col] for col in columns])
    return pd.DataFrame(df, columns=columns)


if __name__ == "__main__":
    df = read_dataframe()
    df["language"] = "Chechen"
    df["glottocode"] = "chec1245"
    df["id_word"] = df["id"]

    df.to_csv("chechen.csv")
