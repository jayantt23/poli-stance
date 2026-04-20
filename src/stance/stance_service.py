from __future__ import annotations

from typing import Any, Dict, List, Optional

import spacy
from transformers import pipeline

from .registry import MOCK_TARGET_REGISTRY, TARGET_REGISTRY, get_aliases, get_related, resolve_target
from .target_extraction import sentence_mentions_any, split_sentences, suggest_targets


def load_nlp_model(model_name: str = "en_core_web_sm"):
    return spacy.load(model_name)


def load_zero_shot_pipeline(
    model_name: str = "facebook/bart-large-mnli", device: int = -1
):
    """
    device = -1 for CPU, 0 for first GPU
    """
    return pipeline("zero-shot-classification", model=model_name, device=device)


def _build_retrieval_names(
    target: str,
    registry: Optional[Dict[str, Dict[str, Any]]],
    retrieval_mode: str = "strict",
) -> List[str]:
    canonical = resolve_target(target, registry)

    aliases = (
        get_aliases(registry or {}, canonical) if registry is not None else [canonical]
    )

    # use strict only! related not available for TARGET_REGISTRY, only the mock, and related is making things somewhat off, like conflating BJP with MODI
    if retrieval_mode == "strict":
        names = aliases

    elif retrieval_mode == "expanded":
        related_names = []
        if registry is not None:
            for rel in get_related(registry, canonical):
                rel_canon = resolve_target(rel, registry)
                related_names.extend(get_aliases(registry, rel_canon))
        names = aliases + related_names
    else:
        raise ValueError("retrieval_mode must be one of: 'strict', 'expanded'")

    seen = set()
    out = []
    for x in names:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            out.append(x)
    return out


def _score_text_for_target(
    text_chunk: str,
    target: str,
    clf,
    include_neutral: bool = True,
) -> Dict[str, float]:
    labels = [
        f"This text supports {target}.",
        f"This text opposes {target}.",
    ]
    if include_neutral:
        labels.append(f"This text is neutral toward {target}.")

    out = clf(text_chunk, labels, multi_label=False)
    raw_scores = dict(zip(out["labels"], out["scores"]))

    mapped = {
        "favor": raw_scores.get(f"This text supports {target}.", 0.0),
        "against": raw_scores.get(f"This text opposes {target}.", 0.0),
    }
    if include_neutral:
        mapped["neutral"] = raw_scores.get(
            f"This text is neutral toward {target}.", 0.0
        )

    return mapped


def _predict_for_target(
    text: str,
    target: str,
    clf,
    nlp,
    registry: Optional[Dict[str, Dict[str, Any]]] = None,
    retrieval_mode: str = "strict",
    top_k_evidence: int = 3,
    include_neutral: bool = True,
    mixed_margin: float = 0.08,
) -> Dict[str, Any]:
    sentences = split_sentences(text, nlp)
    canonical = resolve_target(target, registry)
    names = _build_retrieval_names(canonical, registry, retrieval_mode=retrieval_mode)

    matched_sentences = [s for s in sentences if sentence_mentions_any(s, names)]

    if not matched_sentences:
        return {
            "target": canonical,
            "label": "no_evidence",
            "scores": {},
            "evidence": [],
            "num_sentences_used": 0,
        }

    scored = []
    for sent in matched_sentences:
        score_map = _score_text_for_target(
            sent, canonical, clf, include_neutral=include_neutral
        )
        scored.append((sent, score_map))

    label_keys = ["favor", "against"] + (["neutral"] if include_neutral else [])
    mean_scores = {
        lab: sum(x[1].get(lab, 0.0) for x in scored) / len(scored) for lab in label_keys
    }

    sorted_scores = sorted(mean_scores.items(), key=lambda x: x[1], reverse=True)
    best_label, best_score = sorted_scores[0]
    second_label, second_score = (
        sorted_scores[1] if len(sorted_scores) > 1 else ("", 0.0)
    )

    if abs(best_score - second_score) < mixed_margin:
        final_label = "mixed"
        top_two = {best_label, second_label}
        evidence_scored = []
        for sent, smap in scored:
            evidence_scored.append((sent, max(smap[k] for k in top_two if k in smap)))
        evidence = [
            x[0]
            for x in sorted(evidence_scored, key=lambda x: x[1], reverse=True)[
                :top_k_evidence
            ]
        ]
    else:
        final_label = best_label
        evidence = [
            x[0]
            for x in sorted(
                scored, key=lambda x: x[1].get(final_label, 0.0), reverse=True
            )[:top_k_evidence]
        ]

    return {
        "target": canonical,
        "label": final_label,
        "scores": mean_scores,
        "evidence": evidence,
        "num_sentences_used": len(matched_sentences),
    }


def run_stance_pipeline(
    text: str,
    clf,
    nlp,
    targets: Optional[List[str]] = None,
    registry: Optional[Dict[str, Dict[str, Any]]] = None,
    use_mock_registry: bool = False,
    do_ner_target_suggestion: bool = True,
    retrieval_mode: str = "strict",  # "strict" or "expanded"
    top_k_evidence: int = 3,
    include_neutral: bool = True,
    mixed_margin: float = 0.08,
    country_filter: Optional[str] = None,
    text_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main API for Streamlit / backend integration.

    Inputs
    ------
    text: article / paragraph / tweet
    targets: optional user-provided target array
    registry: optional registry dict
    use_mock_registry: use bundled mock registry if True and registry is None
    do_ner_target_suggestion: whether to auto-generate extra entities
    retrieval_mode: "strict" or "expanded"

    Output
    ------
    JSON-serializable dict with:
      - text_id
      - requested_targets
      - extra_entities
      - results_for_requested_targets
      - results_for_extra_entities
      - all_results
    """
    if registry is None:
        registry = MOCK_TARGET_REGISTRY if use_mock_registry else TARGET_REGISTRY

    requested_targets = targets[:] if targets is not None else []

    extra_entities = []
    if do_ner_target_suggestion:
        auto_targets = suggest_targets(
            text=text,
            nlp=nlp,
            registry=registry,
            use_ner=True,
            use_issue_scan=True,
            country_filter=country_filter,
        )
        requested_canon = {
            resolve_target(t, registry).lower() for t in requested_targets
        }
        for t in auto_targets:
            if t.lower() not in requested_canon:
                extra_entities.append(t)

    requested_canonical = []
    seen = set()
    for t in requested_targets:
        canon = resolve_target(t, registry)
        if canon.lower() not in seen:
            seen.add(canon.lower())
            requested_canonical.append(canon)

    all_targets = requested_canonical + [
        t
        for t in extra_entities
        if t.lower() not in {x.lower() for x in requested_canonical}
    ]

    all_results = []
    for target in all_targets:
        result = _predict_for_target(
            text=text,
            target=target,
            clf=clf,
            nlp=nlp,
            registry=registry,
            retrieval_mode=retrieval_mode,
            top_k_evidence=top_k_evidence,
            include_neutral=include_neutral,
            mixed_margin=mixed_margin,
        )
        all_results.append(result)

    requested_set = {t.lower() for t in requested_canonical}
    results_for_requested_targets = [
        r for r in all_results if r["target"].lower() in requested_set
    ]
    results_for_extra_entities = [
        r for r in all_results if r["target"].lower() not in requested_set
    ]

    return {
        "text_id": text_id,
        "requested_targets": requested_targets,
        "resolved_requested_targets": requested_canonical,
        "extra_entities": extra_entities,
        "results_for_requested_targets": results_for_requested_targets,
        "results_for_extra_entities": results_for_extra_entities,
        "all_results": all_results,
    }


#  result = run_stance_pipeline(
#     text=user_text,
#     clf=clf,
#     nlp=nlp,
#     targets=user_targets_or_none,
#     registry=YOUR_BIG_REGISTRY,
#     do_ner_target_suggestion=auto_generate_targets_flag,
#     retrieval_mode=retrieval_mode,   # "strict" or "expanded"
#     top_k_evidence=3,
#     include_neutral=True,
#     mixed_margin=0.08,
#     country_filter=country_filter_or_none,
#     text_id="streamlit_request_001",
# )
