# Internship Assignment – Data Processing with Python

## Overview
This project demonstrates basic data ingestion, processing, storage, and visualization using Python. 
It includes examples of working with REST APIs, CSV files, SQLite databases, and simple plots.

## Files Included
- api_books.py  
  Fetches book data from a public API and stores it in a local SQLite database.

- student_scores.py  
  Retrieves student test scores, calculates the average score, and visualizes the results using a bar chart.

- csv_to_db.py  
  Reads user information from a CSV file and inserts it into a SQLite database while handling duplicates and missing values.

## Assumptions
- APIs are publicly accessible and return JSON data.
- Data sizes are small enough for local processing.
- SQLite is sufficient for demonstration and testing purposes.

## How to Run
pip install -r requirements.txt
python api_books.py
python students_scores.py
python csv_to_db.py

