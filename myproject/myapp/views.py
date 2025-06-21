from django.shortcuts import render
import pickle
import os
from .sustain import countVectorizer

# Helper function to sort TF-IDF results
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

# Helper function to extract top n keywords
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    sorted_items = sorted_items[:topn]
    results = {}
    for idx, score in sorted_items:
        results[feature_names[idx]] = round(score, 3)
    return results

# Main view handler
def handler(request):
    result = {'no data sent': None}
    if request.method == 'POST':
        sequence = request.POST.get('Name')
        result = get_keywords_text(sequence)
    return render(request, "index.html", {'response': result})

# Keyword extraction logic
def get_keywords_text(docs):
    base_dir = os.path.dirname(__file__)
    tfidf_path = os.path.join(base_dir, 'tfidf.pkl')
    feature_names_path = os.path.join(base_dir, 'feature_names.pkl')

    if not os.path.exists(tfidf_path):
        raise FileNotFoundError(f"tfidf.pkl not found at {tfidf_path}")
    if not os.path.exists(feature_names_path):
        raise FileNotFoundError(f"feature_names.pkl not found at {feature_names_path}")

    with open(tfidf_path, 'rb') as f:
        tfidf_transformer = pickle.load(f)

    with open(feature_names_path, 'rb') as f:
        feature_names = pickle.load(f)

    tf_idf_vector = tfidf_transformer.transform(countVectorizer.transform([docs]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items, topn=10)

    return keywords
