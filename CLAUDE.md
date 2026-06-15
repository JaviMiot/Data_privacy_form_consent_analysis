# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

Research tooling to evaluate Spanish text simplification (Easy-to-Read / Lectura Fácil) quality. Given a CSV with original legal sentences and model-generated simplifications, it computes a battery of NLP metrics and exports a structured Excel report.

## Environment setup

Managed with **uv** (Python 3.12). After cloning:

```bash
uv sync
uv run python -m spacy download es_core_news_sm   # required NLP model
```

## Common commands

```bash
uv run jupyter notebook          # open analysis notebooks
uv run pytest                    # run tests
uv run pytest src/metrics/mer_trans_metrics/tests/calculator_tests.py  # single test file
```

## Architecture

### Metric families

Three independent calculators, each with a `models.py` (Pydantic) and `calculator.py`:

| Module | Class | Metrics |
|---|---|---|
| `src/metrics/mer_trans_metrics/` | `MerTrans` | BLEU, SARI, BERTScore, MeaningBERT, RoBERTaSense-FACIL |
| `src/metrics/clears_metrics/` | `ClearsCalculator` | Cosine TF-IDF, Cosine Embeddings (sentence-transformers) |
| `src/metrics/readability_complexity/` | `index_calculator()` | Orthographic, syllabic, lexical, syntactic indices + classic readability formulas (Fernández-Huerta, INFLESZ, Mu, Polini, Crawford) |

### Orchestrator

`MetricsProcessor` in `src/metrics/process_data.py` drives the full pipeline:

1. Reads a `pd.DataFrame` with mandatory columns `document_id`, `original_sentence_id`, `original_text`, `prediction_text` and optional `simplified_text` (human reference).
2. Detects whether gold references exist (`has_references`). Without them, the original text is used as fallback for reference-dependent metrics.
3. Groups rows by `document_id` and computes metrics per document.
4. Produces two metric sets per document — **orig_\*** (prediction vs. original) and **gold_\*** (prediction vs. gold reference).
5. `save_consolidated_report(output_path)` writes an Excel with three sheets: *Raw Data*, *Summary by Document*, *Metrics Summary*.

The factory lambda at the bottom of `process_data.py` is the intended entry point:
```python
from src.metrics.process_data import metrics_processor
processor = metrics_processor(df)           # ngrams=4 by default
processor.save_consolidated_report("out.xlsx")
```

### Static data (readability module)

`src/metrics/readability_complexity/` bundles:
- `Mapa_indices.xlsx` — thresholds for interpreting each index (read on first call, cached globally).
- `lista_abreviaturas_esp.xlsx` — Spanish abbreviation expansions applied before NLP parsing.
- `palabras_todas.txt` / `palabras_todas_no_conjugaciones.txt` — Spanish word lists for loanword detection.

The readability module also fetches the RAE top-5000 word list at runtime (`corpus.rae.es`). Network failures are silently handled; the loanword index will be empty if the fetch fails.

### Notebooks

`notebooks/` contains four analysis phases:
- `01_first_analysis/` — initial checklist analysis and metric generation.
- `02_second_analysis/` — second-layer analysis.
- `03_e2r_guidelines/` — guideline compliance analysis.
- `04_analize_with_paper_e2r/` — analysis aligned with the FACILE paper (see `papers/FACILE/`).

Each notebook folder stores its own intermediate `.xlsx` outputs.

### Text cleaning

`src/utils.py::clean_text()` normalises raw text (invisible chars, Word/PDF artefacts, smart quotes, punctuation spacing) before feeding it to any metric. Apply it to CSV columns before constructing `MetricsProcessor`.
