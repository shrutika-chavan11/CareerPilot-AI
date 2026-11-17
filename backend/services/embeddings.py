from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.config import settings
class RetrievalEngine:
    def __init__(self):
        self.model = None
        if settings.use_sentence_transformers:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(settings.embedding_model)
            except Exception as e: print("Embedding model unavailable; using TF-IDF:", e)
    def fit(self, docs):
        self.docs = docs
        if not docs: self.matrix = None; return
        if self.model:
            self.matrix = self.model.encode(docs, normalize_embeddings=True)
        else:
            self.vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
            self.matrix = self.vectorizer.fit_transform(docs)
    def search(self, query, k):
        if not self.docs or self.matrix is None: return []
        if self.model:
            q = self.model.encode([query], normalize_embeddings=True)
            scores = (self.matrix @ q[0]).tolist()
        else: scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0].tolist()
        return sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[:k]
@lru_cache(maxsize=1)
def get_retriever(): return RetrievalEngine()
