import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)


def clean_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("-", "_")
        .str.replace(" ", "_")
    )

    return df


def load_csv(file_path, table_name):
    print(f"\nLoading {file_path}...")

    df = pd.read_csv(file_path)

    df = clean_column_names(df)

    # Convert columns to correct numeric types
    for col in df.columns:

        # Keep week columns as text
        if col in ["booking_week", "invoice_week", "collection_week"]:
            continue

        # Convert lag percentages
        if col.startswith("lag_"):

            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

            # 18% -> 0.18
            df[col] = df[col] / 100

        # Convert amount columns
        else:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    print("Columns:", df.columns.tolist())
    print("Rows:", len(df))

    print("\nData Types:")
    print(df.dtypes)

    print("\nSample Data:")
    print(df.head())

    print("\nNull Values:")
    print(df.isnull().sum())

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully.")


if __name__ == "__main__":

    load_csv(
        "data/actual_booking_invoices_collection.csv",
        "actual_booking_invoices_collection"
    )

    load_csv(
        "data/booking_to_invoice_forecasting.csv",
        "booking_to_invoice_forecasting"
    )

    load_csv(
        "data/invoice_to_cash_forecasting.csv",
        "invoice_to_cash_forecasting"
    )