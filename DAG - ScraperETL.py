from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from datetime import datetime
import os
from Bookworm2Scrape.scrapper.scrapper.spiders.etl import library_cleanse, book_cleanse


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

project_root = os.path.join(os.path.abspath(os.getcwd()), f'dags',f'Bookworm2Scrape', f'scrapper')


with DAG(
    dag_id='book_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline to scrape and process book data',
    schedule_interval=None,
    catchup=False,
    tags=['books', 'scrapy', 'etl'],
) as dag:

    remove_old_files = BashOperator(
        task_id='remove_old_files',
        bash_command='python3 scrapper/spiders/remove_files.py',
        cwd=project_root,
    )

    crawl_library = BashOperator(
        task_id='crawl_library_data',
        bash_command=f"scrapy crawl library_data",
        cwd=project_root,
    )


    cleanse_library = BashOperator(
        task_id='cleanse_library',
        bash_command='python3 scrapper/spiders/etl.py library',
        cwd=project_root,
    )

    crawl_books = BashOperator(
        task_id='crawl_book_data',
        bash_command=f"scrapy crawl book_data",
        cwd=project_root,
    )

    cleanse_books = BashOperator(
        task_id='cleanse_books',
        bash_command='python3 scrapper/spiders/etl.py book',
        cwd=project_root,
    )


    remove_old_files >> crawl_library >> cleanse_library >> crawl_books >> cleanse_books
