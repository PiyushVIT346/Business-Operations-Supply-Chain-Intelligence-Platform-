from prefect import flow, task

from etl.extract import extract_data
from etl.transform import clean_orders
from etl.load import load_table

@task
def extract_task():
    return extract_data()

@task
def transform_task(data):
    data["orders"] = clean_orders(data["orders"])
    return data

@task
def load_task(data):
    for table_name, df in data.items():
        load_table(df, table_name)

@flow(name="Business Operations ETL")
def business_pipeline():

    data = extract_task()

    cleaned_data = transform_task(data)

    load_task(cleaned_data)

if __name__ == "__main__":
    business_pipeline()