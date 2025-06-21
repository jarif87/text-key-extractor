from django.core.cache import cache
import pickle
import os

model_cache_key = 'model_cache'

# Construct the absolute path to cv.pkl
cv_path = os.path.join(os.path.dirname(__file__), 'cv.pkl')

# Try retrieving from Django cache
countVectorizer = cache.get(model_cache_key)

if countVectorizer is None:
    if os.path.exists(cv_path):
        try:
            with open(cv_path, 'rb') as f:
                countVectorizer = pickle.load(f)
            cache.set(model_cache_key, countVectorizer, None)
        except MemoryError:
            raise MemoryError("Not enough memory to load cv.pkl. Consider reducing max_features in the vectorizer.")
        except Exception as e:
            raise RuntimeError(f"Error loading cv.pkl: {str(e)}")
    else:
        raise FileNotFoundError(f"CountVectorizer pickle file not found at: {cv_path}")
