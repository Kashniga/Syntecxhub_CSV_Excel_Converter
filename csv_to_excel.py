import pandas as pd
import argparse
import logging
import sys
from pathlib import Path

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# ------------------ Functions ------------------
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info("CSV file loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to read CSV file: {e}")
        sys.exit(1)

def clean_data(df):
    # Handle missing values
    df = df.fillna("")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    logging.info("Data cleaned and normalized.")
    return df

def parse_dates(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            logging.info(f"Parsed dates in column: {col}")
        else:
            logging.warning(f"Date column '{col}' not found.")
    return df

def rename_columns(df, rename_map):
    df = df.rename(columns=rename_map)
    logging.info("Columns renamed.")
    return df

def export_excel(df, output_path):
    try:
        df.to_excel(output_path, index=False, engine="openpyxl")
        logging.info(f"Excel file saved at: {output_path}")
    except Exception as e:
        logging.error(f"Failed to export Excel file: {e}")
        sys.exit(1)

# ------------------ Main ------------------
def main():
    parser = argparse.ArgumentParser(description="CSV to Excel Converter")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output Excel (.xlsx) file path")
    parser.add_argument(
        "--date-columns",
        nargs="*",
        default=[],
        help="Columns to parse as dates"
    )
    parser.add_argument(
        "--rename",
        nargs="*",
        help="Column renames in old=new format"
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        logging.error("Input file does not exist.")
        sys.exit(1)

    df = load_csv(input_file)
    df = clean_data(df)

    if args.date_columns:
        df = parse_dates(df, args.date_columns)

    if args.rename:
        rename_map = {}
        for item in args.rename:
            if "=" in item:
                old, new = item.split("=")
                rename_map[old] = new
        df = rename_columns(df, rename_map)

    export_excel(df, output_file)

if __name__ == "__main__":
    main()
