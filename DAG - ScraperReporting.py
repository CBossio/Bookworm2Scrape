from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

def load_df():
    project_root = os.path.join(os.path.abspath(os.getcwd()), f'dags',f'Bookworm2Scrape', f'scrapper')
    df = pd.read_csv(os.path.join(project_root, "result.csv"))
    return df, project_root

def books_per_category():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    os.makedirs(output_folder, exist_ok=True)
    report = df.groupby("Category")["UPC"].count().reset_index(name="Book_Count").sort_values("Book_Count", ascending=False)
    report.to_excel(os.path.join(output_folder, "books_per_category.xlsx"), index=False)

def best_titles_with_less_stock():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    report = df[df["Stock_quantity"] <= 3].sort_values(by="Rating", ascending=False).head(10)
    report = report[['UPC','Category','Title','Price_Tax','Stock_quantity','Rating','URL']]
    report.to_excel(os.path.join(output_folder, "best_titles_with_less_stock.xlsx"), index=False)

def best_categories_with_less_stock():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    category_stats = df.groupby("Category").agg({"Rating": "mean", "Stock_quantity": "sum"}).reset_index()
    report = category_stats.sort_values(by=["Rating", "Stock_quantity"], ascending=[False, True]).head(10)
    report.to_excel(os.path.join(output_folder, "best_categories_with_less_stock.xlsx"), index=False)

def average_price_per_category():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    report = df.groupby("Category")["Price_No_Tax"].mean().reset_index(name="Average_Price_No_Tax")
    report.to_excel(os.path.join(output_folder, "average_price_per_category.xlsx"), index=False)

def best_expensive_books():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    report = df[df["Rating"] >= 4].sort_values(by=["Price_Tax"], ascending=[False]).head(10)
    report.to_excel(os.path.join(output_folder, "best_expensive_books.xlsx"), index=False)

def best_cheap_books():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    report = df[df["Rating"] >= 4].sort_values(by=["Price_Tax"], ascending=[True]).head(10)
    report.to_excel(os.path.join(output_folder, "best_cheap_books.xlsx"), index=False)

def rating_pie_chart():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    rating_counts = df['Rating'].value_counts().sort_index()
    rating_percentages = rating_counts / rating_counts.sum() * 100
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(rating_percentages, labels=rating_percentages.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
    ax.set_title("Rating Distribution (%)", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "rating_pie_chart.png"), dpi=300)
    plt.close()

def price_range_pie_chart():
    df, project_root = load_df()
    output_folder = os.path.join(project_root, 'reporting_output')
    bins = [0, 10, 20, 30, 40, float('inf')]
    labels = ["< 10", "10-20", "20-30", "30-40", "> 50"]
    df["Price_Range"] = pd.cut(df["Price_Tax"], bins=bins, labels=labels, right=False)
    price_counts = df["Price_Range"].value_counts().sort_index()
    price_percentages = price_counts / price_counts.sum() * 100
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(price_percentages, labels=price_percentages.index, autopct="%1.1f%%", startangle=140, textprops={"fontsize": 12})
    ax.set_title("Price Distribution by Range (with Tax)", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "price_range_pie_chart.png"), dpi=300)
    plt.close()

def create_reporting_dag():
    with DAG(
        dag_id="scraper_reporting_dag",
        schedule_interval=None,
        start_date=datetime(2025, 5, 22),
        catchup=False,
        tags=["reporting"]
    ) as dag:

        tasks = [
            PythonOperator(task_id="books_per_category", python_callable=books_per_category),
            PythonOperator(task_id="best_titles_with_less_stock", python_callable=best_titles_with_less_stock),
            PythonOperator(task_id="best_categories_with_less_stock", python_callable=best_categories_with_less_stock),
            PythonOperator(task_id="average_price_per_category", python_callable=average_price_per_category),
            PythonOperator(task_id="best_expensive_books", python_callable=best_expensive_books),
            PythonOperator(task_id="best_cheap_books", python_callable=best_cheap_books),
            PythonOperator(task_id="rating_pie_chart", python_callable=rating_pie_chart),
            PythonOperator(task_id="price_range_pie_chart", python_callable=price_range_pie_chart),
        ]

        return dag

globals()["scraper_reporting_dag"] = create_reporting_dag()
