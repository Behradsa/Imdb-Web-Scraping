import numpy as np
from collections import Counter
from math import log, sqrt
import pandas as pd

# Sample movie plot summaries
movies_df = pd.read_csv("data\data.csv")
plot_summaries = movies_df["summery"].values.tolist()

# New plot summary to find similar plots
new_plot = "A young hero goes on a quest to save the world."


# Tokenization function
def tokenize(text):
    return text.lower().split()


# Build vocabulary
def build_vocabulary(docs):
    vocab = set()
    for doc in docs:
        vocab.update(tokenize(doc))
    return list(vocab)


# Compute term frequency
def compute_tf(doc, vocab):
    tf = np.zeros(len(vocab))
    word_count = Counter(tokenize(doc))
    for i, term in enumerate(vocab):
        tf[i] = word_count[term]
    return tf


# Compute inverse document frequency
def compute_idf(docs, vocab):
    idf = np.zeros(len(vocab))
    num_docs = len(docs)
    for i, term in enumerate(vocab):
        containing_docs = sum(1 for doc in docs if term in tokenize(doc))
        idf[i] = log((num_docs + 1) / (containing_docs + 1)) + 1  # Smoothing
    return idf


# Compute TF-IDF
def compute_tfidf(tf, idf):
    return tf * idf


# Cosine similarity
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = sqrt(np.dot(vec1, vec1))
    norm_vec2 = sqrt(np.dot(vec2, vec2))
    return dot_product / (norm_vec1 * norm_vec2)


# Build vocabulary
vocabulary = build_vocabulary(plot_summaries)

# Compute IDF
idf_vector = compute_idf(plot_summaries, vocabulary)

# Compute TF-IDF for each plot summary
tfidf_matrix = np.array(
    [compute_tfidf(compute_tf(doc, vocabulary), idf_vector) for doc in plot_summaries]
)

# Compute TF-IDF for the new plot summary
new_plot_tfidf = compute_tfidf(compute_tf(new_plot, vocabulary), idf_vector)

# Find the k nearest neighbors
k = 3
similarities = [
    cosine_similarity(new_plot_tfidf, tfidf_vec) for tfidf_vec in tfidf_matrix
]
nearest_neighbors = np.argsort(similarities)[-k:][::-1]

# Display the results
print(f"Top {k} similar plot summaries to the new plot summary:\n")
for rank, index in enumerate(nearest_neighbors):
    print(f"Rank {rank + 1}:")
    print(f"Plot Summary: {plot_summaries[index]}")
    print(f"Cosine Similarity: {similarities[index]:.4f}")
    print()
