from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

from metrics.clears_metrics.models import CosineTfIdfMetric, CosineEmbeddingMetric, ClearsMetrics

class ClearsCalculator:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def get_cosine_tfidf(self, predictions: list[str], references: list[str]) -> CosineTfIdfMetric:
        """
        Calcula la similitud coseno entre predicciones y referencias usando TF-IDF.
        """
        scores = []
        for pred, ref in zip(predictions, references):
            vectorizer = TfidfVectorizer()
            try:
                tfidf_matrix = vectorizer.fit_transform([pred, ref])
                sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
            except (ValueError, IndexError):
                sim = 0.0  # Si alguno está vacío o falla la vectorización
            scores.append(sim)
        return CosineTfIdfMetric(scores=scores)

    def get_cosine_embeddings(self, predictions: list[str], references: list[str]) -> CosineEmbeddingMetric:
        """
        Calcula la similitud coseno entre predicciones y referencias usando sentence-transformers.
        """
        pred_embs = self.model.encode(predictions, show_progress_bar=False, batch_size=32)
        ref_embs = self.model.encode(references, show_progress_bar=False, batch_size=32)

        scores = []
        for p_emb, r_emb in zip(pred_embs, ref_embs):
            sim = float(cosine_similarity([p_emb], [r_emb])[0][0])
            scores.append(sim)
        return CosineEmbeddingMetric(scores=scores)

    def get_all_metrics(self, predictions: list[str], references: list[str]) -> ClearsMetrics:
        tfidf = self.get_cosine_tfidf(predictions, references)
        embedding = self.get_cosine_embeddings(predictions, references)
        return ClearsMetrics(tfidf=tfidf, embedding=embedding)
