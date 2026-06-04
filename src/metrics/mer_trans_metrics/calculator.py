import evaluate
from nltk.tokenize import word_tokenize
import nltk
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import typing

from src.metrics.mer_trans_metrics.models import BleuMetric, SariMetric, BertScoreMetric, MeaningBertMetric, MerTransMetrics, RobertaSenseFacilMetric

nltk.download('punkt')
nltk.download('punkt_tab')

class MerTrans:
    class RobertaSenseFacilMetric(BaseModel):
        model: typing.Any
        tokenizer: typing.Any

    def __init__(self, ngrams: int = 4):
        self.bleu = evaluate.load("bleu")
        self.sari = evaluate.load("sari")
        self.bertscore = evaluate.load("bertscore")
        self.meaning_bert = evaluate.load("davebulaval/meaningbert")
        self.roberta_sense_facil = self.__init_roberta_sense_facil_metric()
        self.ngrams = ngrams



    def __init_roberta_sense_facil_metric(self):
        """
        https://huggingface.co/oeg/RoBERTaSense-FACIL
        """
        repo = "oeg/RoBERTaSense-FACIL"  
        model = AutoModelForSequenceClassification.from_pretrained(repo)
        tokenizer = AutoTokenizer.from_pretrained(repo)
        model.config.id2label = {
            0: "preserves_meaning",
            1: "does_not_preserve"
        }
        model.config.label2id = {
            "preserves_meaning": 0,
            "does_not_preserve": 1
        }
        return self.RobertaSenseFacilMetric(model = model, tokenizer = tokenizer)

    def get_bleu_metric(self, references: list[str], predictions: list[str]):
        """
        https://github.com/huggingface/evaluate/tree/main/metrics/bleu
        """
        references = [[text] for text in references]
        return BleuMetric(**self.bleu.compute(predictions=predictions, references=references, tokenizer=word_tokenize, max_order=self.ngrams))

    def get_sari_metric(self, sources: list[str], references: list[str], predictions: list[str]):
        """
        https://github.com/huggingface/evaluate/tree/main/metrics/sari
        """
        references = [[text] for text in references]
        return SariMetric(**self.sari.compute(sources=sources, predictions=predictions, references=references))
    
    def get_bert_score(self, references: list[str], predictions: list[str]):
        """
        https://github.com/huggingface/evaluate/blob/main/metrics/bertscore/README.md
        """
        references = [[text] for text in references]
        return BertScoreMetric(**self.bertscore.compute(predictions=predictions, references=references, lang="es", batch_size=64))
    
    def get_meaning_bert_score(self, references: list[str], predictions: list[str]):
        """
        https://huggingface.co/davebulaval/MeaningBERT
        """
        return MeaningBertMetric(**self.meaning_bert.compute(predictions=predictions, references=references))

    def get_roberta_sense_facil_metric(self, sources: list[str], predictions: list[str]):
        if len(sources) != len(predictions):
            raise ValueError("Sources and predictions must have the same length")
        
        source_join = " ".join(sources)
        prediction_join = " ".join(predictions)

        inputs = self.roberta_sense_facil.tokenizer(source_join, prediction_join, return_tensors="pt", truncation=True, max_length=512)

        with torch.no_grad():
            logits = self.roberta_sense_facil.model(**inputs).logits

        probs = logits.softmax(-1).squeeze().tolist()

        return RobertaSenseFacilMetric(**{self.roberta_sense_facil.model.config.id2label[i]: probs[i] for i in range(len(probs))})

    def get_all_metrics_origin(self, sources: list[str], references: list[str], predictions: list[str]):
        return MerTransMetrics(
            bleu=self.get_bleu_metric(sources, predictions),
            sari=self.get_sari_metric(sources, references, predictions),
            bertscore=self.get_bert_score(sources, predictions),
            meaning_bert=self.get_meaning_bert_score(sources, predictions),
            roberta_sense_facil=self.get_roberta_sense_facil_metric(sources, predictions)
        )
    
    def get_all_metrics_gold(self, sources: list[str], references: list[str], predictions: list[str]):
        return MerTransMetrics(
            bleu=self.get_bleu_metric(references, predictions),
            sari=self.get_sari_metric(sources, references, references),
            bertscore=self.get_bert_score(references, predictions),
            meaning_bert=self.get_meaning_bert_score(references, predictions),
            roberta_sense_facil=self.get_roberta_sense_facil_metric(references, predictions)
        )