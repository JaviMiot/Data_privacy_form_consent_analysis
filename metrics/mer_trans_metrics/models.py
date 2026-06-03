import numpy as np
from pydantic import BaseModel, model_validator

class BleuMetric(BaseModel):
    bleu: float
    precisions: list[float]
    brevity_penalty: float
    length_ratio: float
    translation_length: int
    reference_length: int

class SariMetric(BaseModel):
    sari: float

class BertScoreMetric(BaseModel):
    precision: list[float]
    recall: list[float]
    f1: list[float]
    mean_precision: float = 0.0
    mean_recall: float = 0.0
    mean_f1: float = 0.0

    @model_validator(mode='after')
    def compute_means(self):
        self.mean_precision = float(np.mean(self.precision))
        self.mean_recall = float(np.mean(self.recall))
        self.mean_f1 = float(np.mean(self.f1))
        return self

class MeaningBertMetric(BaseModel):
    scores: list[float]
    mean_score: float = 0.0

    @model_validator(mode='after')
    def compute_mean(self):
        self.mean_score = float(np.mean(self.scores))
        return self

class RobertaSenseFacilMetric(BaseModel):
    does_not_preserve: float
    preserves_meaning: float

class MerTransMetrics(BaseModel):
    bleu: BleuMetric
    sari: SariMetric
    bertscore: BertScoreMetric
    meaning_bert: MeaningBertMetric
    roberta_sense_facil: RobertaSenseFacilMetric

