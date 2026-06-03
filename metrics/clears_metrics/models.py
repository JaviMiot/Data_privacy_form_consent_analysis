import numpy as np
from pydantic import BaseModel, model_validator

class CosineTfIdfMetric(BaseModel):
    scores: list[float]
    mean_score: float = 0.0

    @model_validator(mode='after')
    def compute_mean(self):
        self.mean_score = float(np.mean(self.scores))
        return self

class CosineEmbeddingMetric(BaseModel):
    scores: list[float]
    mean_score: float = 0.0

    @model_validator(mode='after')
    def compute_mean(self):
        self.mean_score = float(np.mean(self.scores))
        return self

class ClearsMetrics(BaseModel):
    tfidf: CosineTfIdfMetric
    embedding: CosineEmbeddingMetric
    cosine_avg: float = 0.0

    @model_validator(mode='after')
    def compute_avg(self):
        self.cosine_avg = (self.tfidf.mean_score + self.embedding.mean_score) / 2.0
        return self
