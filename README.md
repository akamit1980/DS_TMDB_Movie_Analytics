# 🎬 TMDB Movie Analytics | End-to-End Data Analytics Project

An end-to-end **Movie Data Analytics project** using Python, Pandas, SQL, MySQL, and Streamlit to explore movie industry data, uncover trends, analyze financial performance, and build an interactive analytics dashboard.

The project demonstrates a complete data analytics workflow, from data cleaning and transformation to SQL-based analysis, exploratory data analysis (EDA), and interactive visualization.

## 📌 Project Overview

The objective of this project is to analyze The Movie Database (TMDB) movie dataset to uncover meaningful insights about movies, genres, ratings, revenue, budgets, actors, directors, and keywords.

The project combines Python-based data analysis with SQL queries and an interactive Streamlit dashboard to make movie data easier to explore and understand.

## 🎯 Project Objectives

- Clean and preprocess raw movie datasets.
- Perform exploratory data analysis using Pandas.
- Use SQL and MySQL to answer business-oriented analytical questions.
- Analyze movie performance based on budget, revenue, and ratings.
- Explore genre popularity and distribution.
- Identify top-performing movies, actors, and directors.
- Build an interactive dashboard with dynamic filters and visualizations.

## 🛠️ Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| SQL | Data querying and analysis |
| MySQL | Relational database management |
| SQLAlchemy | Python-MySQL connectivity |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| Streamlit | Interactive analytics dashboard |
| Jupyter Notebook | Analysis and experimentation |

## 📂 Project Structure

text

```text
DS_TMDB_Movie_Analytics/
│
├── 01_data_cleaning.ipynb
│
├── 02_sql_analysis.ipynb
│
├── 03_pandas_analysis.ipynb
│
├── 04_visualizations.ipynb
│
├── main.py
│
└── README.md
```

## 🔍 Project Workflow

### 1\. Data Cleaning and Preprocessing

Notebook: `01_data_cleaning.ipynb`

This stage focuses on preparing the raw movie datasets for analysis.

Key activities:

- Handling missing and inconsistent values.
- Removing duplicate records where applicable.
- Cleaning column names and data types.
- Preparing movie-related datasets for further analysis.
- Creating cleaned datasets for movies, genres, cast, crew, and keywords.

### 2\. SQL-Based Analysis

Notebook: `02_sql_analysis.ipynb`

SQL is used to perform structured queries and extract meaningful insights from the movie database.

Analytical questions include:

- Which Action movies were released after 2015?
- What are the top 10 highest-grossing movies?
- What are the average budgets and revenues by genre?
- Which actors have appeared in the most movies?
- Which directors have directed more than three movies?
- What are the most frequently used movie keywords?
- Which movies had above-average budgets but below-average revenue?
- Which genres have the highest average ratings?

### 3\. Exploratory Data Analysis Using Pandas

Notebook: `03_pandas_analysis.ipynb`

This stage uses Pandas to explore movie data and identify patterns and relationships.

Areas of analysis include:

- Movie release trends.
- Genre-wise analysis.
- Ratings distribution.
- Budget and revenue comparisons.
- Movie performance analysis.
- Cast and crew exploration.

### 4\. Data Visualization

Notebook: `04_visualizations.ipynb`

Visual representations help communicate analytical findings effectively.

The project uses Matplotlib, Seaborn, and Plotly to explore and present movie-related trends and patterns.

### 5\. Interactive Streamlit Dashboard

File: `main.py`

An interactive dashboard allows users to explore movie data through dynamic filters and visualizations.

**Dashboard features:**

- Global filters for genre, original language, release year, and minimum TMDB rating.
- Movie filtering and tabular exploration.
- KPI cards displaying:
  - Total movies
  - Genres represented
  - Total actors
  - Average movie rating
- Top 10 movies by revenue.
- Genre distribution.
- Budget versus revenue analysis.
- Dynamic analytical insights based on selected filters.
- SQL-powered query exploration through the Queries section.

## 📊 Key Analytical Areas

The project explores the following business and analytical dimensions:

| Area | Analytical Focus |
| --- | --- |
| Movie Performance | Highest-grossing movies |
| Genre Analysis | Genre distribution and performance |
| Financial Analysis | Budget versus revenue |
| Ratings Analysis | Average ratings across genres |
| Cast Analysis | Most frequently appearing actors |
| Crew Analysis | Directors and their movie counts |
| Keyword Analysis | Frequently associated movie keywords |
| Release Trends | Movies released across different years |

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.9+
- MySQL Server
- Jupyter Notebook
- Git

### 1\. Clone the repository

bash

```bash
git clone https://github.com/akamit1980/DS_TMDB_Movie_Analytics.git

cd DS_TMDB_Movie_Analytics
```

### 2\. Create a virtual environment

bash

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

bash

```bash
venv\Scripts\activate
```

**Mac/Linux:**

bash

```bash
source venv/bin/activate
```

### 3\. Install dependencies

bash

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit streamlit-option-menu sqlalchemy pymysql jupyter
```

### 4\. Configure the dataset

The Streamlit application expects the following cleaned CSV files:

text

```text
movies_cleaned.csv
movie_keywords_cleaned.csv
movie_genres_cleaned.csv
genres_cleaned.csv
crew_cleaned.csv
cast_cleaned.csv
```

Update the file paths in `main.py` to match the location of your downloaded or generated CSV files.

### 5\. Configure MySQL

Create a MySQL database:

sql

```sql
CREATE DATABASE tmdb_movie_analytics_project;
```

Import the required cleaned tables into the database.

Configure the database connection in `main.py` using your own MySQL credentials. Use environment variables or a separate configuration file rather than hardcoding passwords.

### 6\. Run the Streamlit application

bash

```bash
streamlit run main.py
```

The application will open in your default browser.

## 📈 Expected Outcomes

By completing this project, users can:

- Understand the end-to-end data analytics lifecycle.
- Apply Python and SQL to real-world analytical problems.
- Extract insights from structured movie datasets.
- Explore relationships between movie budgets, revenue, genres, and ratings.
- Develop interactive dashboards for data-driven exploration.
- Translate raw data into meaningful visual insights.

## 💡 Skills Demonstrated

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Python Programming
- Pandas Data Manipulation
- SQL Query Writing
- MySQL Database Management
- Data Visualization
- Interactive Dashboard Development
- Analytical Thinking and Problem Solving

## 🚀 Future Enhancements

- Add more advanced SQL analytical queries.
- Integrate Power BI or Tableau dashboards.
- Perform predictive analysis for movie revenue.
- Explore genre-wise trends over time.
- Deploy the Streamlit dashboard to a cloud platform.
- Automate the data ingestion and cleaning pipeline.

## 👨‍💻 Author

**Abhinav Kumar Amit**

GitHub: @akamit1980

Project Repository: [DS\_TMDB\_Movie\_Analytics](<https://github.com/akamit1980/DS_TMDB_Movie_Analytics>)

## 📄 Disclaimer

This project is intended for educational and portfolio purposes. Movie data and related trademarks belong to their respective owners. Please refer to the original dataset provider for applicable usage and attribution requirements.

---

⭐ If you find this project useful, feel free to star the repository\!

You can view the [original repository here](<https://github.com/akamit1980/DS_TMDB_Movie_Analytics?utm_source=chatgpt.com>).
