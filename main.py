import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="TMDB Movie Analytics", layout="wide")

# MySQL Database Connection (ready for your Queries tab)
engine = create_engine(
    "mysql+pymysql://root:Omnamahshivay%402026@localhost/tmdb_movie_analytics_project"
)

st.title("TMDB Movie Analytics")


# Load and cache CSV files so the app stays fast when moving sliders
@st.cache_data
def load_data():
    movies_df = pd.read_csv(r"C:\AIML Course\Data\Project1\movies_cleaned.csv")
    movies_keywords_df = pd.read_csv(
        r"C:\AIML Course\Data\Project1\movie_keywords_cleaned.csv"
    )
    movie_genres_df = pd.read_csv(
        r"C:\AIML Course\Data\Project1\movie_genres_cleaned.csv"
    )
    genres_df = pd.read_csv(r"C:\AIML Course\Data\Project1\genres_cleaned.csv")
    crew_df = pd.read_csv(r"C:\AIML Course\Data\Project1\crew_cleaned.csv")
    cast_df = pd.read_csv(r"C:\AIML Course\Data\Project1\cast_cleaned.csv")

    # Clean whitespace from column names across all DataFrames
    for df in [
        movies_df,
        movies_keywords_df,
        movie_genres_df,
        genres_df,
        crew_df,
        cast_df,
    ]:
        df.columns = df.columns.str.strip()

    # Extract release_year if release_date exists
    if (
        "release_date" in movies_df.columns
        and "release_year" not in movies_df.columns
    ):
        movies_df["release_year"] = pd.to_datetime(
            movies_df["release_date"], errors="coerce"
        ).dt.year

    # Dynamically match column names for merging
    movie_col = "movie_id" if "movie_id" in movie_genres_df.columns else "id"
    genre_fk = "genre_id" if "genre_id" in movie_genres_df.columns else "id"
    genre_pk = "id" if "id" in genres_df.columns else "genre_id"

    possible_name_cols = ["name", "genre_name", "genre", "genres", "title"]
    genre_name_col = next(
        (col for col in possible_name_cols if col in genres_df.columns), None
    )

    if genre_name_col is None:
        raise KeyError(
            f"Could not find genre text column. Available columns in genres_cleaned.csv: {genres_df.columns.tolist()}"
        )

    merged_temp = movie_genres_df.merge(
        genres_df,
        left_on=genre_fk,
        right_on=genre_pk,
        how="inner",
        suffixes=("_link", ""),
    )

    merged_genres = merged_temp[[movie_col, genre_name_col]].rename(
        columns={movie_col: "movie_id", genre_name_col: "genre_name"}
    )

    return movies_df, merged_genres, movies_keywords_df, crew_df, cast_df


movies_df, merged_genres, movies_keywords_df, crew_df, cast_df = load_data()

# Detect standard TMDB column names across tables automatically
id_col = "id" if "id" in movies_df.columns else "movie_id"
title_col = "title" if "title" in movies_df.columns else "original_title"
rating_col = (
    "vote_average" if "vote_average" in movies_df.columns else "rating"
)
lang_col = (
    "original_language"
    if "original_language" in movies_df.columns
    else "language"
)
cast_movie_col = "movie_id" if "movie_id" in cast_df.columns else "id"
actor_id_col = (
    "cast_id"
    if "cast_id" in cast_df.columns
    else ("id" if "id" in cast_df.columns else "name")
)

# Single Sidebar Navigation + Global Filter Widgets
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Filter", "Dashboard", "Queries"],
        icons=["funnel", "bar-chart", "database"],
        menu_icon="cast",
        default_index=1,
    )

    st.divider()
    st.subheader("Global Filters")

    # 1. Genre Multiselect
    all_genres = sorted(merged_genres["genre_name"].dropna().unique())
    selected_genres = st.multiselect(
        "Select Genres (leave empty for all)",
        options=all_genres,
        default=[],
    )

    # 2. Language Selectbox
    all_languages = ["All"] + sorted(
        movies_df[lang_col].dropna().unique().tolist()
    )
    selected_language = st.selectbox(
        "Select Original Language", options=all_languages
    )

    # 3. Release-Year Range Slider
    valid_years = movies_df["release_year"].dropna()
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())
    year_range = st.slider(
        "Release Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    # 4. Minimum-Rating Slider
    min_rating = st.slider(
        "Minimum TMDB Rating",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.1,
    )

# Apply Filters Globally (so both Filter and Dashboard pages can use filtered_df)
filtered_df = movies_df[movies_df['release_year'].between(year_range[0], year_range[1])
    & (movies_df[rating_col] >= min_rating)
]

if selected_language != "All":
    filtered_df = filtered_df[filtered_df[lang_col] == selected_language]

if selected_genres:
    matching_movie_ids = merged_genres[
        merged_genres["genre_name"].isin(selected_genres)
    ]["movie_id"].unique()
    filtered_df = filtered_df[filtered_df[id_col].isin(matching_movie_ids)]

# Filter related tables based on the matching movie IDs
filtered_ids = filtered_df[id_col].unique()
filtered_genres = merged_genres[merged_genres["movie_id"].isin(filtered_ids)]
filtered_cast = cast_df[cast_df[cast_movie_col].isin(filtered_ids)]

# ---------------- FILTER PAGE ----------------
if selected == "Filter":
    st.subheader("Filtered Movies Table")
    st.write(f"Showing **{len(filtered_df):,}** matching movies:")
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- DASHBOARD PAGE ----------------
elif selected == "Dashboard":
    st.subheader("Analytics Dashboard")

    if filtered_df.empty:
        st.warning("No movies match your current filter selection.")
    else:
        # 1. KPI Cards
        total_movies = len(filtered_df)
        total_genres = filtered_genres["genre_name"].nunique()
        total_actors = (filtered_cast["actor_name"].nunique()
            if "actor_name" in filtered_cast.columns
            else filtered_cast["person_id_col"].nunique()
        )
        avg_rating = filtered_df[rating_col].mean()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Movies", f"{total_movies:,}")
        kpi2.metric("Genres Represented", f"{total_genres}")
        kpi3.metric("Total Actors", f"{total_actors:,}")
        kpi4.metric("Average Rating", f"{avg_rating:.2f} / 10")

        # 2. Dynamic Text Insight Summary
        genre_rev = filtered_genres.merge(
            filtered_df[[id_col, "revenue"]],
            left_on="movie_id",
            right_on=id_col,
            how="inner",
        )

        if not genre_rev.empty and genre_rev["revenue"].sum() > 0:
            top_genre_row = (
                genre_rev.groupby("genre_name")["revenue"]
                .sum()
                .sort_values(ascending=False)
            )
            top_genre = top_genre_row.index[0]
            top_genre_val = top_genre_row.iloc[0]
            top_movie = filtered_df.sort_values(
                by="revenue", ascending=False
            ).iloc[0]
            st.info(
                f"**Selection Insight:** The highest-grossing genre in this selection is **{top_genre}** "
                f"(${top_genre_val:,.0f} combined revenue), led by **{top_movie[title_col]}**."
            )
        else:
            st.info(
                f"**Selection Insight:** Showing **{total_movies:,}** movies across **{total_genres}** genres "
                f"with an average TMDB rating of **{avg_rating:.2f}**."
            )

        st.divider()

        # 3. Top 10 Movies by Revenue & Genre Distribution
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
                    top_10_rev = filtered_df.nlargest(10, "revenue").sort_values(
                        by="revenue", ascending=True
                    )
                    fig_top10 = px.bar(
                        top_10_rev,
                        x="revenue",
                        y=title_col,
                        orientation="h",
                        title="Top 10 Movies by Revenue",
                        labels={"revenue": "Revenue ($)", title_col: "Movie"},
                        color="revenue",
                        color_continuous_scale="Blues",
                    )
                    fig_top10.update_layout(showlegend=False, coloraxis_showscale=False)
                    st.plotly_chart(fig_top10, use_container_width=True)

        with chart_col2:
                    genre_counts = (
                        filtered_genres["genre_name"].value_counts().reset_index()
                    )
                    genre_counts.columns = ["Genre", "Count"]
                    fig_genre = px.pie(
                        genre_counts,
                        names="Genre",
                        values="Count",
                        hole=0.45,
                        title="Genre Distribution",
                    )
                    fig_genre.update_traces(
                        textposition="inside", textinfo="percent+label"
                    )
                    st.plotly_chart(fig_genre, use_container_width=True)

                # 4. Budget vs Revenue Scatter Plot
        st.subheader("Budget vs. Revenue")
        scatter_df = filtered_df[(filtered_df["budget"] > 0) & (filtered_df["revenue"] > 0)]
        fig_scatter = px.scatter(
                    scatter_df,
                    x="budget",
                    y="revenue",
                    hover_name=title_col,
                    hover_data=["release_year", rating_col],
                    color=rating_col,
                    color_continuous_scale="Viridis",
                    title="Budget vs. Revenue (Excluding $0 Entries)",
                    labels={
                        "budget": "Budget ($)",
                        "revenue": "Revenue ($)",
                        rating_col: "Rating",
                    },
                )
        st.plotly_chart(fig_scatter, use_container_width=True)

        
if selected == "Queries":
    option = st.selectbox(
    "Select a query",
    ("1. List all movies in the Action genre released after 2015, showing title and release date.",
     "2. Find the top 10 highest-grossing movies along with the genre(s) each belongs to.",
     "3. Calculate the average budget and average revenue for each genre, sorted by average revenue descending.",
     "4. List the top 10 actors who have appeared in the most movies in the dataset.(cast)",
     "5. Find all directors who have directed more than 3 movies, along with their movie count.",
     "6. List the top 10 most frequently used keywords across all movies.",
     "7. Find movies where the budget was above the overall average budget but the revenue was below the overall average revenue.",
     "8. List all actors who have appeared in a movie directed by a specific director (e.g., Christopher Nolan).",
     "9. Find the genre with the highest average rating, considering only genres with at least 20 movies.",
     "10. List the top 10 movies with the highest number of keywords tagged to them."),
)
 
    if option == "1. List all movies in the Action genre released after 2015, showing title and release date.":
            query = """
    SELECT title, release_date 
    FROM movies 
    JOIN movie_genres ON movies.movie_id = movie_genres.movie_id 
    JOIN genres ON movie_genres.genre_id = genres.genre_id 
    WHERE genres.genre_name = %s 
      AND YEAR(movies.release_date) > 2015
"""
            df = pd.read_sql(query, params=("Action",), con=engine)

            st.dataframe(df)
            
            if not df.empty:
                df["release_year"] = pd.to_datetime(df["release_date"]).dt.year
                yearly_counts = (
                    df["release_year"]
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )
                yearly_counts.columns = ["Release Year", "Movie Count"]

                fig = px.bar(
                    yearly_counts,
                    x="Release Year",
                    y="Movie Count",
                    text="Movie Count",
                    title="Action Movies Released Per Year (After 2015)",
                )
                fig.update_layout(xaxis=dict(dtick=1))
                st.plotly_chart(fig, use_container_width=True)
    
    if option == "2. Find the top 10 highest-grossing movies along with the genre(s) each belongs to.":
            query = """
    SELECT movies.movie_id, movies.title, movies.revenue, genres.genre_name 
    FROM movies 
    JOIN movie_genres ON movies.movie_id = movie_genres.movie_id 
    JOIN genres ON movie_genres.genre_id = genres.genre_id
    GROUP BY movies.movie_id, movies.title, movies.revenue, genres.genre_name 
    ORDER BY movies.revenue DESC 
    LIMIT 10;
"""
            df = pd.read_sql(query, con=engine)
            st.dataframe(df)
            
            if not df.empty:
                plot_df = df.drop_duplicates(subset=["movie_id"]).copy()
                plot_df["revenue_millions"] = plot_df["revenue"] / 1e6

                fig, ax = plt.subplots(figsize=(9, 5))
                sns.barplot(
                    data=plot_df,
                    x="revenue_millions",
                    y="title",
                    hue="title",
                    palette="viridis",
                    legend=False,
                    ax=ax,
                )
                ax.set_title("Top Highest-Grossing Movies")
                ax.set_xlabel("Revenue ($ Millions)")
                ax.set_ylabel("Movie Title")
                ax.bar_label(ax.containers[0], fmt="$%.0fM", padding=4)
                ax.set_xlim(0, plot_df["revenue_millions"].max() * 1.15)
                plt.tight_layout()

                st.pyplot(fig)
                plt.close(fig)

    
    if option == "3. Calculate the average budget and average revenue for each genre, sorted by average revenue descending.":
        query = """
        SELECT genre_name, AVG(budget) AS avg_budget, AVG(revenue) AS avg_revenue 
        FROM movies 
        JOIN movie_genres ON movies.movie_id = movie_genres.movie_id 
        JOIN genres ON movie_genres.genre_id = genres.genre_id 
        GROUP BY genre_name 
        ORDER BY avg_revenue DESC;
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("Average Budget vs. Average Revenue by Genre")
        st.bar_chart(
        data=df,
        x="genre_name",
        y=["avg_budget", "avg_revenue"],
        stack=False
    )
        
    if option == "4. List the top 10 actors who have appeared in the most movies in the dataset.(cast)":
        query = """
        SELECT 
            actor_name, 
            COUNT(movie_id) AS movie_count 
        FROM `cast` 
        GROUP BY actor_name 
        ORDER BY movie_count DESC 
        LIMIT 10;
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("Top 10 Actors by Movie Count")
        st.bar_chart(
            data=df,
            x="actor_name",
            y="movie_count"
        )
        
    if option == "5. Find all directors who have directed more than 3 movies, along with their movie count.":
        query = """
        SELECT 
            person_name, 
            job, 
            COUNT(movie_id) AS movie_count 
        FROM crew 
        WHERE LOWER(job) = 'director' 
        GROUP BY job, person_name 
        HAVING COUNT(movie_id) > 3 
        ORDER BY movie_count DESC;
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("Directors with More Than 3 Movies")
        st.bar_chart(
            data=df,
            x="person_name",
            y="movie_count",
            horizontal=True,
            sort="-movie_count"
        )

        
    if option == "6. List the top 10 most frequently used keywords across all movies.":
        query = """
            SELECT keyword_name, COUNT(movie_id) AS movie_count
            FROM movie_keywords
            GROUP BY keyword_id, keyword_name
            LIMIT 10;
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("Top 10 Most Frequently Used Keywords")
        st.bar_chart(
        data=df,
        x="keyword_name",
        y="movie_count",
        horizontal=True,
        sort="-movie_count"
    )
        
    if option == "7. Find movies where the budget was above the overall average budget but the revenue was below the overall average revenue.":
        query = """
        SELECT title, budget, revenue 
        FROM movies 
        WHERE budget > (SELECT AVG(budget) FROM movies)
        AND revenue < (SELECT AVG(revenue) FROM movies);  
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("High-Budget, Low-Revenue Movies (Budget vs. Revenue)")
        st.scatter_chart(
        data=df,
        x="budget",
        y="revenue"
    )
    
    if option == "8. List all actors who have appeared in a movie directed by a specific director (e.g., Christopher Nolan).":
        query = """
        SELECT DISTINCT actor_name 
        FROM `cast` as c
        JOIN crew as cr on c.movie_id = cr.movie_id
        WHERE cr.job= 'Director' and cr.person_name = "Christopher Nolan";
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
                
    if option == "9. Find the genre with the highest average rating, considering only genres with at least 20 movies.":
        query = """
        SELECT 
            g.genre_name, 
            ROUND(AVG(m.vote_average), 2) AS avg_rating,
            COUNT(m.movie_id) AS movie_count
        FROM movies m
        JOIN movie_genres mg ON m.movie_id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.genre_id
        GROUP BY g.genre_id, g.genre_name
        HAVING COUNT(m.movie_id) >= 20
        ORDER BY avg_rating DESC;
    """
        df = pd.read_sql(query, con=engine)

    # Highlight the #1 highest-rated genre at the top
        if not df.empty:
            top_genre = df.iloc[0]
            st.metric(
                label="Highest-Rated Genre (Min. 20 Movies)",
                value=top_genre["genre_name"],
                delta=f"{top_genre['avg_rating']} avg rating ({top_genre['movie_count']} movies)"
            )

            st.dataframe(df)

    # Compare all qualifying genres in a sorted horizontal bar chart
        st.subheader("Average Movie Rating by Genre (At Least 20 Movies)")
        st.bar_chart(
            data=df,
            x="genre_name",
            y="avg_rating",
            horizontal=True,
            sort="-avg_rating"
    )

        
    if option == "10. List the top 10 movies with the highest number of keywords tagged to them.":
        query = """
            SELECT 
                m.title, 
                COUNT(mk.keyword_id) AS keyword_count
            FROM 
                movies m
            INNER JOIN 
                movie_keywords mk ON m.movie_id = mk.movie_id
            GROUP BY 
                m.movie_id, m.title
            ORDER BY 
                keyword_count DESC
            LIMIT 10;
    """
        df = pd.read_sql(query, con=engine)
        st.dataframe(df)
        
        st.subheader("Top 10 Movies by Keyword Count")
        st.bar_chart(
        data=df,
        x="title",
        y="keyword_count",
        horizontal=True,
        sort="-keyword_count"
    )