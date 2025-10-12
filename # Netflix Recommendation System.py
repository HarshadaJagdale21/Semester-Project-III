# Netflix Recommendation System
# ----------------------------------------------------------

# Step 1: Import libraries
import pandas as pd

# -----------------------------
# Step 2: Load Netflix dataset
file_path = "netflix_titles.csv"  # Make sure the CSV is in the same folder
df = pd.read_csv(file_path)

# Step 3: Clean dataset (remove rows without description or title)
df_clean = df.dropna(subset=["title", "description"]).reset_index(drop=True)

# -----------------------------
# Step 4: Netflix keyword search function (top 3 results)
def search_netflix(keyword, top_n=3):
    # Filter dataset by keyword in title or description
    filtered_df = df_clean[
        df_clean["title"].str.contains(keyword, case=False, na=False) |
        df_clean["description"].str.contains(keyword, case=False, na=False)
    ]

    # Check if no results found
    if filtered_df.empty:
        return None

    # Sort by rating (descending)
    if "rating" in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by="rating", ascending=False)

    # Return top N results
    return filtered_df[["title", "description", "listed_in", "release_year", "rating"]].head(top_n)

# -----------------------------
# Step 5: Interactive input
keyword = input("Enter a keyword or description to search Netflix shows/movies: ")

# Netflix Results
print(f"\nTop 3 Netflix Results for '{keyword}':")
netflix_results = search_netflix(keyword)
if netflix_results is None:
    print(f"No Netflix shows/movies found for '{keyword}'")
else:
    print(netflix_results)
