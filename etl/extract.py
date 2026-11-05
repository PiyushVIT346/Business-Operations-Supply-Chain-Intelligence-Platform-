import csv
from pathlib import Path

from etl.config import DATA_DIR, TABLE_MAPPING



def validate_files():
    """Check source CSV files and read their headers."""

    print("\n========== EXTRACT VALIDATION ==========\n")

    file_information = {}

    for filename, table_name in TABLE_MAPPING.items():

        file_path = DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing dataset file: {file_path}"
            )

        if file_path.stat().st_size == 0:
            raise ValueError(
                f"Dataset file is empty: {filename}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.reader(file)

            headers = next(reader, None)

        if not headers:
            raise ValueError(
                f"No headers found in {filename}"
            )

        if len(headers) != len(set(headers)):
            raise ValueError(
                f"Duplicate column names found in {filename}"
            )

        if any(not header.strip() for header in headers):
            raise ValueError(
                f"Empty column name found in {filename}"
            )

        file_information[filename] = {
            "table": table_name,
            "headers": headers,
            "size_bytes": file_path.stat().st_size
        }

        print(f"File: {filename}")
        print(f"Target: staging.{table_name}")
        print(f"Columns: {len(headers)}")
        print("Status: Valid\n")

    print("All nine source files passed validation.")

    return file_information