import pandas as pd

from metrics.mer_trans_metrics.calculator import MerTrans


class TestMerTransBLEU:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")


    def test_calculate_metric(self):
        original_text = self.test_data["original_text"].to_list()
        adapted_text = self.test_data["simplified_text"].to_list()
        
        metric = MerTrans()

        result = metric.get_bleu_metric(original_text, adapted_text)
        
        assert result, print(result)

    def test_calculate_metric_of_same_text__should_return_bleu_score_one(self):
        original_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        
        metric = MerTrans()

        result = metric.get_bleu_metric(original_text, adapted_text)
        
        assert result.bleu == 1, print(result)

        original_text = ["hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?",]
        
        result = metric.get_bleu_metric(original_text, adapted_text)
        
        assert result.bleu == 1, print(result)


class TestMerTransSARI:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")


    def test_calculate_metric(self):
        original_text = self.test_data["original_text"].to_list()
        reference_texts = self.test_data["simplified_text"].to_list()
        adapted_text = self.test_data["original_text"].to_list()
        
        metric = MerTrans()

        result = metric.get_sari_metric(original_text, reference_texts, adapted_text)

        assert result, print(result)

    def test_calculate_metric_of_same_text__should_return_bleu_score_one_hundred(self):
        original_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        reference_texts = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        
        metric = MerTrans()

        result = metric.get_sari_metric(original_text, reference_texts, adapted_text)

        assert result.sari == 100, print(result)

        original_text = ["hola como te encuentras?",]
        reference_texts = ["hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?",]
        
        result = metric.get_sari_metric(original_text, reference_texts, adapted_text)
        
        assert result.sari == 100, print(result)


class TestMerTransBertScore:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")


    def test_calculate_metric(self):
        original_text = self.test_data["original_text"].to_list()
        adapted_text = self.test_data["simplified_text"].to_list()
        
        metric = MerTrans()

        result = metric.get_bert_score(original_text, adapted_text)
        
        assert result, print(result)

    def test_calculate_metric_of_same_text__should_return_bleu_score_one(self):
        original_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        
        metric = MerTrans()

        result = metric.get_bert_score(original_text, adapted_text)
        
        assert result.precision == [1, 1, 1,], print(result)
        assert result.mean_precision == 1.0, print(result)
        assert result.mean_f1 == 1.0, print(result)

        original_text = ["hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?",]
        
        result = metric.get_bert_score(original_text, adapted_text)
        
        assert result.precision == [1,], print(result)
        assert result.mean_precision == 1.0, print(result)


class TestMerTransMeaningBertScore:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")


    def test_calculate_metric(self):
        original_text = self.test_data["original_text"].to_list()
        adapted_text = self.test_data["simplified_text"].to_list()
        
        metric = MerTrans()

        result = metric.get_meaning_bert_score(original_text, adapted_text)
        
        assert result, print(result)

    def test_calculate_metric_of_same_text__should_return_bleu_score_one(self):
        original_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?","hola como te encuentras?","hola como te encuentras?",]
        
        metric = MerTrans()

        result = metric.get_meaning_bert_score(original_text, adapted_text)

        assert result.scores == [100, 100, 100,], print(result)
        assert result.mean_score == 100, print(result)

        original_text = ["hola como te encuentras?",]
        adapted_text = ["hola como te encuentras?",]
        
        result = metric.get_meaning_bert_score(original_text, adapted_text)
        
        assert result.scores == [100,], print(result)
        assert result.mean_score == 100, print(result)


class TestMerTransAllMetrics:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")

    def test_get_all_metrics(self):
        original_text = self.test_data["original_text"].to_list()[:5]
        reference_text = self.test_data["simplified_text"].to_list()[:5]
        adapted_text = self.test_data["simplified_text"].to_list()[:5]
        
        metric = MerTrans()
        result = metric.get_all_metrics(original_text, reference_text, adapted_text)
        
        assert result.bleu
        assert result.sari
        assert result.bertscore
        assert result.meaning_bert


class TestMerTransRobertaSenseFacilMetric:
    test_data = pd.read_csv("es_trial_document.csv", encoding="utf-8")

    def test_calculate_metric_with_data_from_csv__should_return_a_result(self):
        original_text = self.test_data["original_text"].to_list()
        adapted_text = self.test_data["simplified_text"].to_list()
        
        metric = MerTrans()
        result = metric.get_roberta_sense_facil_metric(original_text, adapted_text)

        assert result, print(result)
    
    def test_calculate_metric_with_example_text__should_return_a_result(self):
        original = "El lobo, que parecía amable, engañó a Caperucita."
        adapted  = """El lobo parecía amable.
            El lobo engañó a Caperucita.
            """
        
        metric = MerTrans()
        result = metric.get_roberta_sense_facil_metric([original], [adapted])

        assert result, print(result)
        