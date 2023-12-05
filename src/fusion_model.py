import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

data = pd.read_csv('recipes.csv')

# Preprocesses
tokenizer = Tokenizer(filters='--')  # Pisah-pisahin tiap bahan di Ingredients
tokenizer.fit_on_texts(data['ingredients'])
vocab_size = len(tokenizer.word_index) + 1
sequences = tokenizer.texts_to_sequences(data['ingredients'])
max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Struktur Model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=50, input_length=max_len),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(vocab_size, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])