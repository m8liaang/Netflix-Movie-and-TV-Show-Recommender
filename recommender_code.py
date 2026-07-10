# Import needed Python packages
import pandas as pd
import numpy as np
import random

# Read CSV file
netflix_entertainment = pd.read_csv('https://raw.githubusercontent.com/datacamp/community-groupby/refs/heads/master/data/chasewillden-netflix-shows/data/netflix.csv')

# Preprocess and prepare the data
netflix_entertainment.info()

netflix_entertainment.head()

netflix_entertainment.tail()

netflix_entertainment = netflix_entertainment.drop(columns=['ratinglevel', 'ratingdescription', 'user_rating_score', 'user_rating_size'])
netflix_entertainment = netflix_entertainment.sort_values(by='release_year')
netflix_entertainment = netflix_entertainment.drop_duplicates(subset=['title'])

netflix_entertainment.nunique()

netflix_entertainment['rating'].unique()
netflix_entertainment['rating'] = netflix_entertainment['rating'].replace('UR', 'Unrated')

# To view the minimum and maximum years in CSV: print(netflix_entertainment['release_year'].min(), netflix_entertainment['release_year'].max())
release_years = np.arange(1940, 2018).tolist()

# RECOMMEND A TV SHOW/MOVIE

def recommended_show_movie():

  recommended = netflix_entertainment.sample()

  return recommended

# NETFLIX MOVIE AND TV SHOW RECOMMENDER

# List of accepted search answers
movie_answers = ['movie', 'movies']
tv_answers = ['tv show', 'tv', 'tv shows', 'television', 'television show', 'television shows']

movie_ratings = ['g', 'pg', 'pg-13', 'r', 'unrated']
tv_ratings = ['tv-y7', 'tv-y', 'tv-y7-fv', 'tv-g','tv-14', 'tv-pg', 'tv-ma']

# Main Search Function
def search_function():

  print("Welcome to the Netflix Movie and TV Show Recommender, which has movies and TV shows from 1940 to 2017!")

  search = input("Would you like to watch a movie or a TV show? ").lower().strip()

  if search in movie_answers:
    format_type = 'movie'
    return rating(netflix_entertainment, format_type)

  elif search in tv_answers:
    format_type = 'tv'
    return rating(netflix_entertainment, format_type)

  else:
    print("Please pick one: movies or TV shows.")
    return search_function()

# Movie/TV Show Rating Search Function
def rating(initial_df, media_format):

  if media_format == 'movie':
    allowed_ratings = movie_ratings
    options = 'G, PG, PG-13, R, or Unrated'
    format_prompt = 'movie'

  else:
    allowed_ratings = tv_ratings
    options = 'TV-Y7, TV-Y, TV-Y7-FV, TV-G, TV-14, TV-PG, TV-MA'
    format_prompt = 'TV show'

  print(f"\nNow, pick the rating the {format_prompt} should have.")

  rating_search = input(f"Please pick one of the following ({options}) or write 'any' if you have no preference: ").lower().strip()

  if rating_search == 'any':
    new_df = initial_df[initial_df["rating"].str.lower().isin(allowed_ratings)]
    return year_range(new_df, media_format)

  elif rating_search in allowed_ratings:
    new_df = initial_df[initial_df["rating"].str.lower() == rating_search]
    return year_range(new_df, media_format)

  else:
    print(f"Invalid selection. Please select from {options} or 'any'.")
    return rating(initial_df, media_format)

# Year Range Search Function
def year_range(new_df, format_prompt):

  while True:

    start_year = input(f"Finally, pick a range of release years you would like the {format_prompt} to be from. Write 'any' if you have no preference. Release year start date (1940 to 2017): ").lower().strip()

    if start_year == 'any':
      return new_df

    try:

      start_year = int(start_year)

      if not (1940 <= start_year <= 2017):
        print("Please enter a year between 1940 and 2017.")
        continue

      end_year = input(f"{format_prompt.capitalize()} year range end date (1940 to 2017): ").lower().strip()

      end_year = int(end_year)

      if not (1940 <= end_year <= 2017):
        print("Please enter a year between 1940 and 2017.")
        continue

      if end_year < start_year:
        print("End year must be greater than or equal to start year.")
        continue

      return new_df[new_df["release_year"].between(start_year, end_year)]

    except ValueError:
      print("Please enter a valid year.")

# RUN FUNCTION/SEE RESULTS

recommended_show_movie()

search_function()
