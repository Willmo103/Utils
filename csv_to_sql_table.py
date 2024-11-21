# File Name: csv_to_sql_model.py
# Relative Path: ./csv_to_sql_model.py
# Date: 2024-10-22
# Description: Python script to read a CSV file, create a SQL table, and insert all records into an MSSQL database using SQLAlchemy.

import pandas as pd
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import urllib

# Load environment variables from .env file
load_dotenv()

# Function to read a CSV file and create a corresponding SQL table, then insert all records into the database
def csv_to_sql(file_path):
    try:
        # Get the database URL and table prefix from environment variables
        db_url = os.getenv("MSSQL_DB_URL")
        table_prefix = os.getenv("TABLE_PREFIX", "")
        if not db_url:
            raise ValueError("MSSQL_DB_URL not found in environment variables. Please set it in your .env file.")

        # Ensure correct MSSQL driver is used in the connection string
        if "mssql+pyodbc" not in db_url:
            raise ValueError("Invalid driver. Make sure to use 'mssql+pyodbc' in your MSSQL_DB_URL with the appropriate driver.")
        
        # Example for db_url: mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

        # Determine file type and read the file
        if not file_path.endswith('.csv'):
            raise ValueError("Unsupported file type. Use CSV files only.")

        df = pd.read_csv(file_path)
        
        data_types_mapping = {
            'int64': Integer,
            'float64': Float,
            'object': String,
            'datetime64[ns]': DateTime
        }

        # Create SQLAlchemy engine and metadata
        engine = create_engine(db_url)
        metadata = MetaData()
        
        # Create a table based on the CSV file
        base_table_name = os.path.splitext(os.path.basename(file_path))[0].lower()
        table_name = f"{table_prefix}{base_table_name}"
        columns = [Column('id', Integer, primary_key=True, autoincrement=True)]

        for column in df.columns:
            dtype = str(df[column].dtype)
            sql_type = data_types_mapping.get(dtype, String)
            columns.append(Column(column, sql_type))

        table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)  # Create the table in the database

        # Insert data into the table
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Convert DataFrame to dictionary records for insertion
        records = df.to_dict(orient='records')
        with engine.connect() as connection:
            connection.execute(table.insert(), records)
        
        print(f"Table '{table_name}' created and data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Interactive input for file path
    file_path = input("Enter the file path for the CSV file: ")
    csv_to_sql(file_path)

# Dependency installation: 
# - pandas for data frame manipulation
# - SQLAlchemy for creating and interacting with the database
# - python-dotenv for loading environment variables
# - pyodbc for connecting to MSSQL
# You can install dependencies by running:
# pip install pandas sqlalchemy python-dotenv pyodbc
