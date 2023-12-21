import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load dataset
df = pd.read_csv('../data/final/final_dataset.csv')

df['Ingredients'] = df['Ingredients'].fillna('')

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Ingredients'])

knn_model = NearestNeighbors(algorithm='auto', metric='cosine').fit(tfidf_matrix)

# Get ID recommendations
def get_recommendations(recipe_id, knn_model, n, start, end):
    # Returns recommended recipe id from index start to end
    idx = df[df['id'] == recipe_id].index[0]
    print(idx)
    recipe_tfidf_vector = tfidf_matrix[idx]
    _, indices = knn_model.kneighbors(recipe_tfidf_vector, n_neighbors=n+1)
    similar_recipe_indices = indices.flatten()[1:]
    # Starting index at 1
    similar_recipe_id = df.iloc[similar_recipe_indices]['id'][start-1:end]
    return similar_recipe_id.tolist()

if __name__ == '__main__':
    recipes = [1]
    for r in recipes: 
        print(get_recommendations(r, knn_model, 100, 1, 20))
        print(get_recommendations(r, knn_model, 100, 21, 40))
        print(get_recommendations(r, knn_model, 100, 41, 60))
        print(get_recommendations(r, knn_model, 100, 61, 80))
        print(get_recommendations(r, knn_model, 100, 81, 100))