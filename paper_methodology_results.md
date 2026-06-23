# Section 4 — Methodology

## 4.1 Research Corpus and Gold Standard

The empirical study is grounded in a corpus of **ten data-protection and consent forms** (GDPR-compliant privacy notices and image/video authorisation documents) collected from Spanish public institutions, universities, research groups, and organisations specialising in Easy-to-Read (E2R) adaptation. These documents were selected because they represent a widespread genre of legally mandated communication that must be understood by citizens of all literacy levels — including people with intellectual disabilities, elderly adults, and non-native speakers — yet is routinely produced in dense, formulaic legal language. Their structural complexity is governed by the Spanish Data Protection Agency (AEPD) model clauses guide, which prescribes the information epigraphs that must appear in any compliant data-protection notice.

In addition to the ten source forms, two paired image/video authorisation documents were collected in both their original version and an expert-adapted E2R version produced by qualified Lectura Fácil practitioners. These paired documents serve a dual purpose: (i) as the input for all automated adaptation tools to process, and (ii) as the **gold standard** for computing reference-based automatic metrics (BLEU, BERTScore, MeaningBERT, and RoBERTa Sense Facil). Using an expert-adapted reference allows the study to assess not only the degree to which each tool's output differs from the original (ORIG_\* metrics) but also how closely it approaches human-quality E2R adaptation (GOLD_\* metrics).

The structural requirements for both layers of each adapted document were defined in accordance with the AEPD model clauses guide and the UNE 153101:2018 EX standard, which jointly specify what information must be present and at what level of detail.

---

## 4.2 E2R Guideline Compliance Profiling of Source Documents

The UNE 153101:2018 EX standard defines **60 E2R guideline codes** distributed across four linguistic dimensions: typography and special characters (§6.1), vocabulary and terminology (§6.2), grammar and syntax (§6.3), and document structure and presentation (§6.4). The standard's prescriptions range from formatting rules (e.g., avoiding uppercase text) to deep syntactic constraints (e.g., avoiding passive voice, gerunds, and incidental clauses).

To establish the baseline E2R compliance of the source corpus before any adaptation was attempted, each of the ten source documents was analysed to identify which UNE guideline codes its text violates. The annotation relied on **FACILE's built-in "Identify Guidelines" tool**, which automatically flags document fragments that violate specific UNE codes. The automatically generated annotations were subsequently **manually validated** by the authors, who confirmed, corrected, or rejected each flagged instance. For each validated violation, the annotated fragment was recorded together with the corresponding guideline code and its description. The resulting annotations were exported to `guidelines_analysis.xlsx`, which contains one sheet per document (columns: *Code*, *Guideline name*, *Non-compliant fragment*) and one reference sheet mapping all 60 codes to their descriptions.

This profiling step serves to quantify how far the source forms deviate from the E2R standard before any automated tool is applied, providing an empirically grounded motivation for the adaptation task and a characterisation of the linguistic challenges the tools must address.

---

## 4.3 E2R Adaptation Tool Classification

Eleven tools were evaluated across three groups defined by their interaction paradigm and technical underpinning (Table 4.1). The taxonomy was designed to capture the main deployment scenarios in which E2R adaptation could realistically be carried out today.

**Table 4.1 — E2R Adaptation Tool Classification**

| Group | Label | Description | Tools |
|---|---|---|---|
| **G1** | Pre-parameterized Conversational Agents | ChatGPT-based assistants built and configured by E2R experts; the user submits text directly with no prompt engineering required | Placea; Asistente Antonio Gonzales Crespo; Asistente Mark Jonathan Camacho Escatel; Asistente Francisco Javier Alvarez Jimenez |
| **G2** | General-Purpose Foundation Models | State-of-the-art LLMs accessed in their native interface; a uniform zero-shot prompt derived from UNE 153101 requirements was applied to all models | Gemini 3.1 Pro; GPT 5.4 Think; Claude Sonnet 4.6; deepseek-v3.2 |
| **G3** | Normative and Standardized Approaches | Tools designed explicitly for E2R or fine-tuned on parallel E2R corpora; used according to each tool's own documentation | FACILE; SimpleText (ClearText); Modelo\_Qwen3.5\_9B |

**Group 1** simulates the practitioner-level deployment scenario: a domain expert has configured a conversational agent with E2R knowledge, and an end-user with no NLP expertise can submit text and receive an adapted output without any additional intervention. All four G1 tools are built on top of OpenAI GPT models but operate as "black boxes" that encapsulate the E2R expertise of their designers.

**Group 2** represents the scenario of an expert user who interacts directly with a general-purpose language model. To ensure a fair and reproducible comparison, a single zero-shot prompt was constructed from the key requirements of the UNE 153101 guidelines and applied uniformly to all four models. This design choice deliberately isolates the contribution of the underlying model from that of the prompting strategy.

**Group 3** encompasses tools that encode E2R rules explicitly or have been trained on paired original-to-E2R corpora. FACILE is a semi-automatic system that combines a rule base with NLP components and is oriented towards supporting E2R experts in the adaptation workflow. SimpleText (ClearText) applies a pipeline of rule-based linguistic modules. Modelo\_Qwen3.5\_9B is a 9-billion-parameter model fine-tuned on a Spanish parallel corpus of original texts aligned with their expert E2R adaptations, representing the supervised fine-tuning paradigm.

---

## 4.4 Tool Processing Protocol

Each of the eleven tools was applied to the same set of source documents following the protocol appropriate for its group:

- **G1:** Source text was submitted directly through each tool's conversational interface. No additional prompting, configuration, or post-processing was performed; the tool's internal parameterization was the sole adaptation mechanism.
- **G2:** A single zero-shot prompt, constructed from the normative requirements of UNE 153101:2018 EX, was prepended to the source text and submitted uniformly to all four models via their respective APIs or chat interfaces. The same prompt was used for every document and every G2 model.
- **G3:** Each tool was operated according to its official documentation. FACILE was used through its semi-automatic web interface; SimpleText (ClearText) was applied via its NLP pipeline; Modelo\_Qwen3.5\_9B was queried through its inference API with no additional prompting beyond the source text.

The output of each tool was collected as plain text. All outputs were passed through the `clean_text()` utility (`src/utils.py`) to normalise invisible characters, smart quotes, punctuation spacing, and document artefacts introduced by PDF or Word export before any metric was computed.

---

## 4.5 Quantitative Evaluation: Automatic NLP Metrics

Five automatic metrics were computed for each tool's output, covering both lexical overlap and semantic fidelity:

- **BLEU** (Papineni et al., 2002): 4-gram precision between the adaptation output and the original text, computed via SacreBLEU. Although BLEU was originally designed for machine translation, it is included here for comparability with prior work; its known limitation of penalising paraphrase-heavy outputs should be borne in mind when interpreting values.
- **SARI** (Xu et al., 2016): the primary adaptation quality metric, which jointly measures the quality of addition, deletion, and keeping operations by comparing the output against both the original and the reference simultaneously. Higher SARI values indicate that the tool performs more appropriate lexical and syntactic transformations.
- **BERTScore F1** (Zhang et al., 2020): computes token-level cosine similarity between contextual embeddings of the adaptation output and the original, using multilingual BERT. It captures meaning preservation independently of lexical overlap, making it complementary to SARI.
- **MeaningBERT** (Devaraj et al., 2021): a regression model fine-tuned on human meaning-preservation judgements for text adaptation, returning a score in [0, 100]. Higher values indicate better preservation of the original meaning.
- **RoBERTa Sense Facil**: a meaning-preservation classifier trained on Spanish E2R data, returning the probability that the adaptation preserves the meaning of the original (`preserves_meaning` ∈ [0, 1]).

All metrics were computed using the `MetricsProcessor` class (`src/metrics/process_data.py`) under Python 3.12, with `bert-score 0.3.13`, `sacrebleu 2.6`, and `sentence-transformers 5.3`. Two evaluation modes were computed for each tool: scores against the **original text** (ORIG\_\*) and scores against the **gold reference** adaptation (GOLD\_\*). The ORIG\_\* scores measure how much the tool's output departs from the source; the GOLD\_\* scores measure how closely it approximates the expert adaptation.

---

## 4.6 Qualitative Evaluation: Legal Information Completeness Checklist

Automatic NLP metrics capture surface and semantic transformation but cannot determine whether legally required information is present in the adapted output. To assess this dimension, a **15-item compliance checklist** was developed from the AEPD model clauses guide for GDPR privacy notices. The checklist is organised into five categories:

1. **Identificación** (1 item): identification of the data controller
2. **Estructura** (1 item): two-layer document structure (Capa 1 + Capa 2)
3. **Básica — Capa 1** (6 items): six mandatory epigraphs in the summary layer (purpose, legal basis, recipients, rights brief, data source, usage rules)
4. **Garantías** (1 item): conditions and usage constraints
5. **Adicional — Capa 2** (6 items): detailed information in the expanded layer (contact details of controller and DPO, retention period, automated decision-making, full rights exercise procedure, complaint reference to AEPD)

The two-layer structure follows the UNE 153101:2018 EX recommendation that E2R documents present a concise summary (Capa 1, pages 1–3) followed by a detailed "More information" section (Capa 2, pages 4+). This structure is critical for legal compliance: Capa 1 must convey the essential information in accessible language, while Capa 2 provides the full legal detail required by GDPR.

Each checklist item was scored on a three-point scale: **1** = fully present and correctly formatted; **0.5** = partially present or incorrectly formatted; **0** = absent. Scoring was performed independently for each of the ten source documents processed by each tool, and the final **Compliance (%)** score for each tool is the mean across all documents:

> Compliance (%) = (Σ item scores / 15) × 100

The checklist was validated against the expert E2R reference adaptation, which achieved 100% compliance, confirming that all 15 items are attainable.

---
---

# Section 5 — Results

## 5.1 E2R Guideline Violations in Source Documents

Before any automated adaptation was attempted, the ten source forms were analysed for compliance with the UNE 153101:2018 EX standard. The annotation process, described in §4.2, identified **514 violations** distributed across **36 of the 60** UNE guideline codes, yielding an average of 51.4 violations per document. This high baseline non-compliance rate empirically confirms that standard GDPR forms present a substantive E2R adaptation challenge for all evaluated tools.

Table 5.1 lists the ten most frequently violated guidelines. The most prevalent violation is **6.1.8** (avoid parentheses, brackets, and unusual symbols such as %, &, and /), recorded 57 times across the corpus. This reflects the pervasive use of legal shorthand and symbolic notation in GDPR forms. Close behind is **6.2.4** (avoid abstract, technical, or complex terms, 48 violations), confirming that specialised legal vocabulary is the dominant lexical barrier to E2R accessibility. Uppercase text (6.1.1, 41 violations) and adverbs in *-mente* (6.2.7, 36 violations) complete the typography-vocabulary cluster. The syntactic dimension is also strongly represented: reflexive passive (6.3.5, 31) and active passive (6.3.4, 30) together account for 61 violations, with compound and subjunctive tenses (6.3.3, 27) and incidental clauses (6.3.13, 23) further increasing the syntactic complexity load.

**Table 5.1 — Top-10 Violated UNE 153101 Guideline Codes Across the Source Corpus**

| Rank | Code | Violations | Guideline |
|---|---|---|---|
| 1 | 6.1.8 | 57 | Avoid parentheses, brackets, and unusual symbols (%, &, /) |
| 2 | 6.2.4 | 48 | Avoid abstract, technical, or complex terms |
| 3 | 6.1.1 | 41 | Avoid uppercase letters |
| 4 | 6.2.7 | 36 | Avoid adverbs ending in *-mente* |
| 5 | 6.3.5 | 31 | Avoid reflexive passive voice |
| 6 | 6.3.4 | 30 | Avoid passive voice |
| 7 | 6.2.11 | 29 | Avoid abbreviations |
| 8 | 6.3.3 | 27 | Avoid compound tenses, conditionals, and subjunctives |
| 9 | 6.3.13 | 23 | Avoid incidental clauses enclosed by commas |
| 10 | 6.2.12 | 20 | Avoid acronyms |

The distribution of violations is markedly uneven. The top ten codes alone account for 342 of the 514 total violations (66.5%), while the 26 remaining violated codes together contribute only 172 instances. This concentration suggests that targeted interventions addressing typography normalisation, lexical substitution, and passive-to-active transformation would resolve the majority of E2R non-compliance in this document type.

The dominant violation categories align with the most challenging features for automated systems to address without degrading semantic fidelity. Symbol and uppercase violations (6.1.1, 6.1.8, 6.2.11, 6.2.12) are in principle amenable to rule-based preprocessing, whereas lexical complexity (6.2.4) and syntactic restructuring (6.3.3, 6.3.4, 6.3.5, 6.3.13) require generative transformation that inherently risks omitting or distorting the original meaning. This tension between accessibility and faithfulness underpins the interpretation of all subsequent results.

---

## 5.2 Legal Information Completeness: Checklist Compliance

### 5.2.1 Overall Compliance by Tool

Table 5.2 presents the checklist compliance scores for all eleven tools and the expert gold reference, ranked in descending order. The gold reference achieves 100% compliance, confirming that the 15-item checklist correctly captures all mandatory legal information requirements and that full compliance is attainable.

**Table 5.2 — Legal Information Completeness (Compliance %) by Tool**

| Group | Tool | Items Fulfilled / 15 | Compliance (%) |
|---|---|---|---|
| Gold | Lectura Fácil [Referencia] | 15.0 | 100.00 |
| G1 | Asistente Antonio Gonzales Crespo | 14.5 | 96.67 |
| G3 | SimpleText (ClearText) | 14.5 | 96.67 |
| G2 | Claude Sonnet 4.6 | 14.0 | 93.33 |
| G2 | GPT 5.4 Think | 14.0 | 93.33 |
| G2 | deepseek-v3.2 | 14.0 | 93.33 |
| G3 | FACILE | 14.0 | 93.33 |
| G1 | Placea | 13.5 | 90.00 |
| G1 | Asistente Mark Jonathan Camacho Escatel | 13.5 | 90.00 |
| G1 | Asistente Francisco Javier Alvarez Jimenez | 13.5 | 90.00 |
| G2 | Gemini 3.1 Pro | 13.0 | 86.67 |
| G3 | Modelo\_Qwen3.5\_9B | 12.0 | 80.00 |

> *Verify these values against `table_5_2_checklist_compliance.xlsx` generated by the checklist notebook before final submission.*

### 5.2.2 Group-Level Patterns

At group level, G1 (pre-parameterized agents) and G2 (foundation models) achieve identical average compliance (91.67%), while G3 (normative approaches) averages 90.00%. However, the within-group variance tells a more nuanced story.

Within G1, the spread from 90.00% (three agents) to 96.67% (Asistente Antonio) is modest, suggesting that expert parameterization produces reliably complete outputs regardless of which assistant is used. The high compliance of Asistente Antonio is likely attributable to explicit structural reminders in its system prompt that address the two-layer requirement and all mandatory GDPR epigraphs.

Within G2, Gemini 3.1 Pro (86.67%) underperforms relative to the other three models (all 93.33%), despite receiving an identical zero-shot prompt. This within-group variance indicates that the models differ in their capacity to follow structured instructions consistently across multiple documents. The three higher-scoring G2 models — Claude Sonnet 4.6, GPT 5.4 Think, and deepseek-v3.2 — demonstrate that UNE-grounded zero-shot prompting can achieve compliance levels comparable to expert-configured agents.

Within G3, the contrast between SimpleText (96.67%) and Modelo\_Qwen3.5\_9B (80.00%) is striking. SimpleText's rule-based architecture, which operates on explicit structural templates, successfully preserves all required legal epigraphs. Modelo\_Qwen3.5\_9B's lower score suggests that its fine-tuning corpus prioritised linguistic style and accessibility features over structural completeness, resulting in adapted outputs that are linguistically simpler but may omit legally required sections.

### 5.2.3 Layer 1 vs. Layer 2 Analysis

The most revealing pattern in the checklist results is the systematic gap between Capa 1 (basic information layer) and Capa 2 (detailed information layer) compliance. Layer 1 items — identification, purpose, legal basis, recipients, rights brief, and usage rules — achieve near-perfect compliance across all tools, with most tools scoring 1.0 on each item. By contrast, Layer 2 items show substantially lower compliance across the board.

The two most violated items are "Detalle legal" (detailed legal references for each epigraph, 7.0 total non-compliant instances across all tools) and "Dos capas diferenciadas" (explicit two-layer document structure, 3.5 non-compliant instances). The "Dos capas diferenciadas" violation is particularly consequential: without a clear structural separation between the summary layer and the detailed layer, users cannot navigate the document to locate the information relevant to their needs. This failure appears across all three groups, indicating that the two-layer document architecture prescribed by UNE 153101 is not a naturally emergent property of any of the evaluated approaches and would require explicit structural constraints to be reliably achieved.

---

## 5.3 Automatic Adaptation Quality Metrics

### 5.3.1 Results by Group

Table 5.3 reports the group-average scores across the five automatic metrics, computed against the original text (ORIG\_\*) together with the mean checklist compliance. For reference, the gold standard's GOLD\_\* metric values are also reported.

**Table 5.3 — Group Averages Across Automatic NLP Metrics**

| Group | SARI | BERTScore F1 | MeaningBERT | RoBERTa Sense | Compliance (%) |
|---|---|---|---|---|---|
| G1: Conversational Agents | 46.71 | 0.744 | 87.43 | 0.991 | 91.67 |
| G2: Foundation Models | 50.78 | 0.760 | 85.18 | 0.988 | 91.67 |
| G3: UNE Standard | 41.81 | 0.875 | 93.14 | 0.972 | 90.00 |
| Gold reference (GOLD\_\*) | — | 0.722 | 74.50 | 0.982 | 100.00 |

> *Verify against `table_5_3_group_averages.xlsx` generated by the tools notebook before final submission.*

G2 achieves the highest SARI (50.78), indicating that general-purpose foundation models with UNE-grounded prompting produce the most extensive lexical and syntactic transformation relative to the source. G3, by contrast, achieves the highest BERTScore F1 (0.875) and MeaningBERT (93.14), indicating that normative tools preserve the semantic content of the original more faithfully, even if their outputs depart less from the surface form of the source.

A key reference point is the **gold standard's GOLD\_\* metric values**. The expert E2R reference achieves a BERTScore F1 of only 0.722 against the original — lower than any of the three tool groups' ORIG\_BERTScore averages. This apparent paradox reflects the nature of expert E2R adaptation: a human practitioner rewrites the text so extensively (restructuring sentences, replacing technical terms, adding explanations) that the output is lexically and syntactically distant from the source. The fact that all automated tool groups achieve higher ORIG\_BERTScore values than the expert reference suggests that the tools are preserving more of the original surface form, which is consistent with their substantially lower ORIG\_MeaningBERT values compared to the gold reference's GOLD\_MeaningBERT profile.

### 5.3.2 Best Tool per Group

Table 5.4 presents the best-performing tool within each group, selected by primary sort on SARI and secondary sort on Compliance.

**Table 5.4 — Best-Performing Tool per Group**

| Group | Tool | SARI | BERTScore F1 | MeaningBERT | RoBERTa Sense | Compliance (%) |
|---|---|---|---|---|---|---|
| G1 | Asistente Francisco Javier Alvarez Jimenez | 50.64 | 0.752 | 86.85 | 0.990 | 90.00 |
| G2 | deepseek-v3.2 | 53.38 | 0.761 | 84.52 | 0.990 | 93.33 |
| G3 | Modelo\_Qwen3.5\_9B | 44.70 | 0.752 | 90.37 | 0.990 | 80.00 |

> *Verify against `table_5_4_best_per_group.xlsx` generated by the tools notebook before final submission.*

Within G1, the Asistente Francisco Javier Alvarez Jimenez achieves a SARI of 50.64 — fully competitive with Claude Sonnet 4.6 (50.29) and GPT 5.4 Think (50.16) from G2 — despite requiring no user effort in prompt design. This result supports the hypothesis that expert-configured conversational agents can match the adaptation quality of direct LLM interaction, effectively democratising access to LLM-based E2R adaptation for practitioners without NLP expertise.

Within G2, deepseek-v3.2 leads with a SARI of 53.38 and a compliance score of 93.33%, making it the highest-performing individual tool on the primary ranking metric while also maintaining strong legal completeness. Within G3, Modelo\_Qwen3.5\_9B (SARI 44.70) outperforms the rule-based FACILE (39.66) and SimpleText (41.08) on SARI, confirming that fine-tuning on parallel E2R corpora enables the model to learn transformation patterns — particularly lexical substitution and syntactic restructuring — that explicit symbolic rules cannot readily capture.

### 5.3.3 Gold Reference Benchmark

When evaluated against the expert gold reference (GOLD\_\* metrics), the tool groups exhibit a different profile. The gold BERTScore F1 (0.722) and MeaningBERT (74.50) are notably lower than the ORIG\_\* values, reflecting the structural distance of expert E2R rewriting from the source. Despite this, SimpleText (ClearText) achieves the highest ORIG\_BERTScore (0.9496) and FACILE the second highest (0.9247), suggesting that G3 normative tools produce outputs that are semantically closer to the original than those of G1 or G2 — a profile that may be advantageous in high-stakes legal contexts where preserving the precise meaning of each clause is paramount.

---

## 5.4 Stability and Cross-Metric Consistency

To complement the per-metric analysis, a **stability index** was computed for each tool as the standard deviation of its normalised metric scores across all dimensions (SARI, BERTScore F1, MeaningBERT, RoBERTa Sense, and Compliance, each rescaled to [0, 1]). A lower standard deviation indicates a more balanced, consistent performance profile; a higher value indicates that the tool excels on some metrics at the expense of others.

The Pearson correlation between SARI and the stability index was computed to test whether tools that achieve higher adaptation quality (SARI) tend to show greater cross-metric inconsistency. A statistically significant negative correlation would suggest a fundamental trade-off between adaptation depth and metric balance.

> *Report the Pearson r and p-value from the `table_5_5_stability.xlsx` output and the scatter plot (Fig. 5) here.*

G3 tools tend to show greater stability — consistent with their rule-based or corpus-constrained design, which prevents any single dimension from being prioritised over others. G2 foundation models show wider stability variance: deepseek-v3.2, while leading on SARI, may exhibit a less balanced profile than the more conservative G3 tools. This distinction is practically relevant for use-case selection: for applications where consistent, broadly adequate performance is required across all quality dimensions (e.g., a production system evaluated on multiple criteria simultaneously), a more stable tool may be preferable to a higher-SARI but uneven performer.

---

## 5.5 Integrated Analysis: Adaptation Quality vs. Legal Completeness

Figure 4 (the 2×2 global comparison panel) and the group results from §5.2 and §5.3 jointly reveal that no single tool Pareto-dominates across both adaptation quality (SARI) and legal completeness (Compliance). This decoupling is the central finding of the study.

deepseek-v3.2 achieves the highest SARI (53.38) but does not gain a compliance advantage over simpler tools; its 93.33% compliance is matched by FACILE, Claude Sonnet 4.6, and GPT 5.4 Think. SimpleText (ClearText) presents the inverse profile: it achieves the joint-highest compliance (96.67%, tied with Asistente Antonio) and the highest BERTScore (0.9496), but its SARI of 41.08 places it among the lowest-performing tools on adaptation depth. This suggests that SimpleText's rule-based architecture excels at preserving both the legal structure and the semantic content of the original but generates outputs that are less linguistically transformed.

G1 pre-parameterized agents occupy a practically compelling position in this trade-off space. Their average SARI (46.71) is competitive with individual G2 models, their compliance average (91.67%) matches G2, and they require zero user effort in prompting or configuration. For organisations that need to deploy E2R adaptation workflows at scale without NLP expertise, G1 agents represent the most accessible option without sacrificing substantial quality.

The use-case implications of these findings can be summarised as follows:

- **If legal completeness is the primary criterion** (e.g., compliance audit, regulatory submission): SimpleText (ClearText) or Asistente Antonio Gonzales Crespo offer the highest compliance with strong semantic preservation.
- **If adaptation depth (lexical and syntactic transformation) is the primary criterion** (e.g., maximising readability for cognitively diverse readers): deepseek-v3.2 or Asistente Francisco Javier Alvarez Jimenez offer the highest SARI with acceptable compliance.
- **If deployment simplicity is a constraint**: G1 pre-parameterized agents deliver competitive performance across both dimensions with no prompt engineering requirement.
- **If semantic faithfulness is paramount**: G3 normative tools (FACILE, SimpleText) offer the best BERTScore and MeaningBERT profiles, at the cost of lower transformation depth.

These recommendations are necessarily conditioned on the characteristics of the evaluated corpus (GDPR forms in Spanish) and the specific UNE 153101:2018 EX standard; generalisability to other legal genres or other national E2R standards would require further empirical investigation.

---

*Numbers in Tables 5.2–5.5 are reproduced from the notebook-generated Excel outputs (`table_5_2_checklist_compliance.xlsx`, `table_5_3_group_averages.xlsx`, `table_5_4_best_per_group.xlsx`, `table_5_5_stability.xlsx`). Verify all values against those files before final submission.*
