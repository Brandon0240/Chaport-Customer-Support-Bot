from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from app.category.category_docs import category_docs


category_docs_flat = {category: ' '.join(docs) for category, docs in category_docs.items()}


vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(category_docs_flat.values())


def route_category_tfidf(question, threshold=0.54):

    query_tfidf = vectorizer.transform([question])

    cosine_similarities = query_tfidf @ tfidf_matrix.T
    cosine_similarities = cosine_similarities.toarray().flatten()

    print(f"Cosine similarities: {cosine_similarities}")

    best_category_index = np.argmax(cosine_similarities)
    best_score = cosine_similarities[best_category_index]


    if best_score >= threshold:
        return list(category_docs_flat.keys())[best_category_index]
    else:
        print("No strong match found. Using general handler.")
        return None


