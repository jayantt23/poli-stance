## Stance

Under `src/stance/`:

- `registry.py`
  - Stores the political target registry(currently it is just a mock, need to make a more updated list).
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

### Running Tests

To run the current unit tests(no tests for loading model and testing it here, given that was developed in Kaggle):

```bash
pytest -q tests/test_registry.py tests/test_target_extraction.py
```
