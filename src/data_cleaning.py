"""
this script loads the raw sales dataset, cleans it, and saves a processed version.

cleaning steps:
- standardize column names (lowercase, underscores).
- strip whitespace from product name and category text fields.
- remove rows with missing or invalid price/quantity values.
- remove negative prices and quantities, which are data entry errors.
"""

import pandas as pd

# define input and output
# point to the raw data and where to save the cleaned data
raw_path = "data/raw/sales_data_raw.csv"
processed_path = "data/processed/sales_data_clean.csv"


# this function loads a csv into a dataframe
# i used copilot to generate the basic idea and added the print
def load_data(file_path: str):
    print("Loading:", file_path)
    return pd.read_csv(file_path)


# this function standardizes column names
# makes column names easier to work with later in analysis
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


# this function handles missing and invalid price/qty values
# converts them to numbers, drops missing, and removes negative values
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    # convert price and qty to numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

    # drop rows where price or qty are missing
    df = df.dropna(subset=["price", "qty"])

    # drop rows with negative price or qty (invalid sales)
    df = df[(df["price"] >= 0) & (df["qty"] >= 0)]

    return df


# load the raw sales data
# need the raw dataset in memory before we can clean it
df = load_data(raw_path)

# standardize column names first so we have prodname, category, price, qty, date_sold
df = clean_column_names(df)

# strip whitespace from text fields
# avoids duplicate-looking values like "Shoes " vs "Shoes"
df["prodname"] = df["prodname"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()

# handle missing and invalid numeric values
df = remove_invalid_rows(df)

# save the cleaned dataset
# store a clean version in data/processed for later analysis
df.to_csv(processed_path, index=False)
print("Saved cleaned file to:", processed_path)
