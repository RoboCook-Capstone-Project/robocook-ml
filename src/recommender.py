import pandas as pd 
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load dataset
df = pd.read_csv('./data/final/final_dataset.csv')

df['Ingredients'] = df['Ingredients'].fillna('')

def custom_tokenizer(text):
    return text.split("--")

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Ingredients'])

# Get ID recommendations
def get_recommendations(recipe_id, start, end):
    # Returns recommended recipe id from index start to end
    # Starting index at 1
    idx = df[df['id'] == recipe_id].index[0]
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = np.argsort(cosine_similarities)[::-1]
    filtered_indices = [i for i in similar_indices if not np.isclose(cosine_similarities[i], 1.0).any()] # Filter out same recipes
    filtered_indices = filtered_indices[start-1:end]
    similar_recipes = [(df.loc[i, 'id']) for i in filtered_indices]
    return similar_recipes

def get_ingredients(recipe_id):
    recipe_row = df[df['id'] == recipe_id]
    if not recipe_row.empty:
        title = recipe_row['Title'].values[0]
        ingredients = recipe_row['Ingredients'].values[0]
        return title, ingredients


recipes = [1]

for r in recipes: 
    recommendations = get_recommendations(r, 1, 5)
    print(r)
    title, recipe = get_ingredients(r)
    print(f"Title: {title}")
    print(f"Ingredients: {recipe}")
    print("----- Recommended Dish -----")
    for recipe_id in recommendations:
        print(f"Recipe ID: {recipe_id}")
    print("----- -----")
    
# Code Testing 
# recipe_id_1 = random.randint(1, 2060) # Ayam
# recipe_id_2 = random.randint(2061, 3848) # Ikan
# recipe_id_3 = random.randint(3849, 6110) # Kambing
# recipe_id_4 = random.randint(6111, 8180) # Sapi
# recipe_id_5 = random.randint(8181, 10209) # Tahu
# recipe_id_6 = random.randint(10210, 12242) # Telur
# recipe_id_7 = random.randint(12243, 14306) # Tempe
# recipe_id_8 = random.randint(14307, 15641) # Udang

# recipes = [recipe_id_1, recipe_id_2, recipe_id_3, recipe_id_4, recipe_id_5, recipe_id_6, recipe_id_7, recipe_id_8]

# for r in recipes: 
#     recommendations = get_recommendations(r)
#     print(r)
#     title, recipe = get_ingredients(r)
#     print(f"Title: {title}")
#     print(f"Ingredients: {recipe}")
#     print("----- Recommended Dish -----")
#     for recipe_id, title, ingredients, cosine_similarity in recommendations:
#         print(f"Recipe ID: {recipe_id}\nTitle: {title}\nIngredients: {ingredients}\nCosine Similarity: {cosine_similarity}")
#     print("----- -----")