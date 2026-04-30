## Ideology Predictor  

Under `src/ideology/`:

### roberta_ideology_predictor.ipynb
- Contains the fine-tuning pipeline for the ideology classification model  
- Uses a transformer-based architecture (RoBERTa)  
- Handles preprocessing, tokenization, training, and evaluation  

### predictor.py
- Provides the `IdeologyPredictor` class for inference  
- Loads the fine-tuned model from Hugging Face  
- Exposes a simple `predict(text)` API  

## Current Pipeline  

The ideology predictor supports:

- input text (sentence / paragraph / article)  
- classification into:
  - Left  
  - Center  
  - Right  
- probability distribution over all classes  
- confidence score for the predicted label  
- reusable pipeline object (used by Evidence Extractor)

The fine-tuned model has also been hosted on [HuggingFace](https://huggingface.co/vriddhi-07/ideology_predictor_roberta).

## Output Format  

The predictor returns a JSON-like dictionary with:

- `ideology_label` – predicted class (Left / Center / Right)  
- `confidence` – score of predicted class  
- `probs_full` – probability distribution over all classes  
- `pipeline` – classifier object (used for downstream tasks)  

## Stance

Under `src/stance/`:

- `registry.py`
  - Stores the political target registry (currently it is just a mock, needs to be expanded).
  - Maps canonical targets to aliases and related entities.
  - Used for alias resolution such as `Modi -> Narendra Modi`, `Didi -> Mamata Banerjee`.

- `target_extraction.py`
  - Handles sentence splitting, NER-based target suggestion, issue keyword detection, and target matching.
  - Supports both user-provided targets and auto-generated targets from text.

- `stance_service.py`
  - Main stance analysis pipeline.
  - Accepts input text, optional target list, registry, and retrieval mode.
  - Returns JSON-like output with:
    - requested targets
    - extra detected entities
    - per-target stance labels
    - stance scores
    - evidence sentences

## Current Pipeline

The current pipeline supports:

- input text  
- optional user-provided target list  
- optional automatic target generation using NER + registry issue keywords  
- registry-backed alias matching  
- strict vs expanded retrieval  
- per-target stance scoring with evidence extraction  

The stance model is currently used in a zero-shot NLI setup:

- premise = sentence/text chunk  
- hypotheses = support / oppose / neutral with respect to a target  

## Output Format

The main API returns a JSON-serializable dictionary with:

- `requested_targets`  
- `resolved_requested_targets`  
- `extra_entities`  
- `results_for_requested_targets`  
- `results_for_extra_entities`  
- `all_results`  

Each target result contains:

- `target`  
- `label`  
- `scores`  
- `evidence`  
- `num_sentences_used`  

---

## Framing

Under `src/framing/`:

- `analyzer.py`
  - Implements the framing analysis component.
  - Uses a transformer-based model to classify the dominant narrative frame in the input text.
  - Identifies how the issue is being presented (e.g., economic, governance, conflict, social justice).
  - Outputs both the predicted frame label and a confidence score.

## Framing Pipeline

The framing module supports:

- input text (article, paragraph, or statement)  
- transformer-based inference for frame classification  
- integration with ideology and stance components  

Unlike stance detection, framing focuses on **how an issue is presented**, not the position taken toward a specific target.

## Output Format (Framing)

The framing module returns:

- `frame`: predicted dominant frame label  
- `confidence`: confidence score  

This output is used downstream by the explanation engine to improve interpretability and reasoning.

---

## Notes

- Stance and framing capture different aspects of political text:

  - **Stance** → position toward a target  
  - **Framing** → how the issue is structured or contextualized  

- Framing helps explain *why* a piece of text may appear left/right/center, especially when stance is mixed or ambiguous.

---

## Explanation Engine

**Location:** `src/explanation/engine.py`

The Explanation Engine acts as the final synthesis layer for the entire Poli-Stance pipeline. Unlike the upstream predictive modules that classify raw text, this module functions as a reasoning engine. It translates the discrete outputs of the classification pipeline into a coherent, academically rigorous, and human-readable justification.

### Core Features

* `Generative AI Integration:` Loads a generative Large Language Model (`Qwen/Qwen2.5-3B-Instruct`) from Hugging Face, utilizing 4-bit NF4 quantization for maximum VRAM efficiency.
* `State Contract Assembly:` Takes the aggregated "State Contract" (ideology, confidence, evidence, stances, and frame) from upstream modules and builds a strict Chain-of-Thought prompt.
* `Ideological Disentanglement:` Enforces strict logical boundaries, ensuring the model separates sentiment directed toward specific entities from the underlying policy frames.
* `Zero-Shot Prompting:` Utilizes zero-shot instruction prompting to force grounded, analytical reasoning.
* `Structured Output:` Generates strict JSON responses to prevent LLM hallucination and ensure seamless compatibility with the frontend dashboard.

### Output Format

The module returns a parsed JSON dictionary containing the following rationale breakdown:

```json
{
  "classification": "The final predicted ideology label.",
  "base_reasoning": "An explanation of how the detected frame, target stances, and extracted evidence mathematically support the classification.",
  "contrastive_reasoning": "An explicit logical statement detailing why the text does NOT align with the opposing ideology (or why it rejects extremes, if Center).",
  "confidence_note": "An analysis of the classifier's confidence score, specifically highlighting ambiguity or moderation if the score is below 0.80.",
  "rationale": "A concise 1-2 sentence executive summary synthesizing the above logic for the end-user."
}
```


## Running Tests

To run the current unit tests (no tests for model loading or inference, since those were developed in Kaggle):

```bash
pytest -q tests/test_registry.py tests/test_target_extraction.py
