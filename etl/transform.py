import pandas as pd
import logging

#from config import DATA_DIR, PROCESSED_DIR, TABLE_MAPPING
from etl.config import DATA_DIR, PROCESSED_DIR, TABLE_MAPPING
logger = logging.getLogger(__name__)


def process_csv_files():

    print("\n========== DATA TRANSFORMATION STARTED ==========")

    quality_report = []

    for filename, table_name in TABLE_MAPPING.items():

        raw_file = DATA_DIR / filename
        processed_file = PROCESSED_DIR / filename

        print(f"\nProcessing: {filename}")

        if not raw_file.exists():
            raise FileNotFoundError(
                f"Raw file not found: {raw_file}"
            )

        # Read all columns as strings to preserve source values
        df = pd.read_csv(
            raw_file,
            dtype=str,
            keep_default_na=False
        )

        original_rows = len(df)

        # Check original column names
        if df.columns.duplicated().any():
            raise ValueError(
                f"Duplicate column names in {filename}"
            )

        # Clean whitespace without changing column names
        for column in df.columns:

            df[column] = df[column].map(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

            # Convert whitespace-only values to empty strings
            df[column] = df[column].replace(
                r"^\s*$",
                "",
                regex=True
            )

        # Calculate blank values per column
        blank_values = int(
            (df == "").sum().sum()
        )

        # Count completely duplicated rows for reporting only
        duplicate_rows = int(
            df.duplicated().sum()
        )

        # Save processed file
        df.to_csv(
            processed_file,
            index=False,
            encoding="utf-8"
        )

        quality_report.append({
            "file_name": filename,
            "table_name": table_name,
            "total_rows": original_rows,
            "total_columns": len(df.columns),
            "blank_values": blank_values,
            "duplicate_rows": duplicate_rows,
            "processed_file": str(processed_file)
        })

        print(f"Rows: {original_rows}")
        print(f"Columns: {len(df.columns)}")
        print(f"Blank values: {blank_values}")
        print(f"Duplicate rows (reported, not removed): {duplicate_rows}")
        print(f"Saved: {processed_file}")

    # Save quality report
    report_df = pd.DataFrame(quality_report)

    report_path = PROCESSED_DIR / "data_quality_report.csv"

    report_df.to_csv(
        report_path,
        index=False,
        encoding="utf-8"
    )

    print("\n========== TRANSFORMATION COMPLETED ==========")
    print(f"Quality report saved at: {report_path}")

    return report_df