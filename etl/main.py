import logging

from etl.extract import validate_files
from etl.transform import process_csv_files
from etl.load import load_csv_files

from etl.config import LOG_DIR


logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    try:
        print("\n========== ETL PIPELINE STARTED ==========")

        # STEP 1: Validate raw files
        print("\nSTEP 1: Validating raw files...")
        validate_files()

        # STEP 2: Transform raw files
        print("\nSTEP 2: Processing CSV files...")
        process_csv_files()

        # STEP 3: Load processed files into PostgreSQL
        print("\nSTEP 3: Loading processed data into PostgreSQL...")
        load_csv_files()

        print("\n========== ETL PIPELINE COMPLETED ==========")

        logging.info("ETL pipeline completed successfully.")

    except Exception as error:

        logging.exception("ETL pipeline failed.")

        print("\nETL PIPELINE FAILED")
        print(f"Error: {error}")

        raise


if __name__ == "__main__":
    run_pipeline()