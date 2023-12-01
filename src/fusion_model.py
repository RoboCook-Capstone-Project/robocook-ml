import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the dataset
data = pd.read_csv('recipes.csv')

# Preprocess the data
tokenizer = Tokenizer(filters='--')  # Customizing filters to handle '--'
tokenizer.fit_on_texts(data['ingredients'])
vocab_size = len(tokenizer.word_index) + 1

# Convert ingredients to sequences
sequences = tokenizer.texts_to_sequences(data['ingredients'])
max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Build a simple recommendation model
input_recipe_1 = Input(shape=(max_len,))
input_recipe_2 = Input(shape=(max_len,))

embedding_layer = Embedding(input_dim=vocab_size, output_dim=50, input_length=max_len)

recipe_1_embedding = embedding_layer(input_recipe_1)
recipe_2_embedding = embedding_layer(input_recipe_2)

flatten_layer = Flatten()

recipe_1_flat = flatten_layer(recipe_1_embedding)
recipe_2_flat = flatten_layer(recipe_2_embedding)

concatenated = Concatenate()([recipe_1_flat, recipe_2_flat])

dense_layer = Dense(128, activation='relu')(concatenated)
output_layer = Dense(vocab_size, activation='softmax')(dense_layer)

model = Model(inputs=[input_recipe_1, input_recipe_2], outputs=output_layer)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model (assuming labels are the same as input sequences)
model.fit([padded_sequences, padded_sequences], sequences, epochs=10, batch_size=32, validation_split=0.2)

# Extract embeddings for recipes
recipe_embeddings = embedding_layer.predict(padded_sequences)

# Function to recommend recipes based on input recipes
def recommend_recipes(recipe1, recipe2, top_n=5):
    input_sequences = tokenizer.texts_to_sequences([recipe1, recipe2])
    input_padded = pad_sequences(input_sequences, maxlen=max_len, padding='post')
    
    input_embeddings = embedding_layer.predict(input_padded)
    
    similarity_matrix = cosine_similarity(input_embeddings)
    
    # Find the most similar recipes
    indices = similarity_matrix[0].argsort()[-top_n-1:-1][::-1]
    
    recommended_recipes = data.iloc[indices]
    
    return recommended_recipes[['name', 'type', 'ingredients']]

# Example usage
recipe1 = "Chicken Masala"
recipe2 = "Fish and Chips"

recommendations = recommend_recipes(recipe1, recipe2)
print(recommendations)
