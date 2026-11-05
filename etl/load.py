import csv
import psycopg2

from psycopg2 import sql


from etl.config import DB_CONFIG, PROCESSED_DIR, TABLE_MAPPING
#from config import DB_CONFIG, PROCESSED_DIR, TABLE_MAPPING

def get_connection():
    """Connect to PostgreSQL."""

    return psycopg2.connect(**DB_CONFIG)


def get_table_columns(cursor, table_name):
    """Read the existing PostgreSQL table columns."""

    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'staging'
          AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table_name,)
    )

    return [row[0] for row in cursor.fetchall()]


def load_csv_files():
    """Refresh staging tables from the source CSV files."""

    print("\n========== STAGING LOAD ==========\n")

    conn = get_connection()

    try:
        with conn:

            with conn.cursor() as cursor:

                # Check every destination table and CSV header
                validated_files = []

                for filename, table_name in TABLE_MAPPING.items():

                    file_path = PROCESSED_DIR / filename

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8-sig",
                        newline=""
                    ) as file:

                        headers = next(csv.reader(file))

                    db_columns = get_table_columns(
                        cursor,
                        table_name
                    )

                    if not db_columns:
                        raise ValueError(
                            f"Missing table: staging.{table_name}"
                        )

                    if set(headers) != set(db_columns):
                        raise ValueError(
                            f"Column mismatch in {filename}.\n"
                            f"CSV columns: {headers}\n"
                            f"DB columns: {db_columns}"
                        )

                    validated_files.append(
                        (filename, table_name, headers)
                    )

                # Refresh only staging tables
                for _, table_name, _ in validated_files:

                    cursor.execute(
                        sql.SQL(
                            "TRUNCATE TABLE {}.{}"
                        ).format(
                            sql.Identifier("staging"),
                            sql.Identifier(table_name)
                        )
                    )

                # Load CSV files
                for filename, table_name, headers in validated_files:

                    file_path = PROCESSED_DIR / filename

                    copy_query = sql.SQL(
                        """
                        COPY {}.{} ({})
                        FROM STDIN
                        WITH (
                            FORMAT CSV,
                            HEADER TRUE,
                            ENCODING 'UTF8',
                            NULL '',
                            QUOTE '"',
                            ESCAPE '"'
                        )
                        """
                    ).format(
                        sql.Identifier("staging"),
                        sql.Identifier(table_name),
                        sql.SQL(", ").join(
                            sql.Identifier(column)
                            for column in headers
                        )
                    )

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8-sig",
                        newline=""
                    ) as file:

                        cursor.copy_expert(
                            copy_query.as_string(conn),
                            file
                        )

                    loaded_rows = cursor.rowcount

                    print(
                        f"Loaded staging.{table_name}: "
                        f"{loaded_rows:,} rows"
                    )

        print("\nAll staging tables loaded successfully.")

    except Exception:
        # Roll back the entire refresh if any table fails
        conn.rollback()
        raise

    finally:
        conn.close()