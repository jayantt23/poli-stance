from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .registry import resolve_target


def split_sentences(text: str, nlp) -> List[str]:
    doc = nlp(text)
    return [s.text.strip() for s in doc.sents if s.text.strip()]


def suggest_targets_from_ner(text: str, nlp) -> List[str]:
    doc = nlp(text)
    ents = []
    for ent in doc.ents:
        if ent.label_ in {"PERSON", "ORG"}:
            ents.append(ent.text.strip())

    seen = set()
    out = []
    for x in ents:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            out.append(x)
    return out


def suggest_targets_from_registry_issues(
    text: str,
    registry: Dict[str, Dict[str, Any]],
    country_filter: Optional[str] = None,
) -> List[str]:
    text_low = text.lower()
    hits: List[str] = []

    for canonical, meta in registry.items():
        if country_filter is not None and meta.get("country") != country_filter:
            continue
        if meta.get("kind") != "issue":
            continue

        for alias in meta.get("aliases", []):
            if alias.lower() in text_low:
                hits.append(canonical)
                break

    seen = set()
    out = []
    for x in hits:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            out.append(x)
    return out


def suggest_targets(
    text: str,
    nlp,
    registry: Optional[Dict[str, Dict[str, Any]]] = None,
    use_ner: bool = True,
    use_issue_scan: bool = True,
    country_filter: Optional[str] = None,
) -> List[str]:
    """
    Returns canonical targets where possible.
    Unknown NER targets are kept as raw strings.
    """
    out: List[str] = []

    if use_ner:
        ner_targets = suggest_targets_from_ner(text, nlp)
        for t in ner_targets:
            out.append(resolve_target(t, registry))

    if use_issue_scan and registry is not None:
        out.extend(
            suggest_targets_from_registry_issues(
                text, registry, country_filter=country_filter
            )
        )

    seen = set()
    deduped = []
    for x in out:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            deduped.append(x)
    return deduped


def compile_patterns(names: List[str]) -> List[re.Pattern]:
    patterns = []
    for name in names:
        patterns.append(
            re.compile(r"\b" + re.escape(name) + r"\b", flags=re.IGNORECASE)
        )
    return patterns


def sentence_mentions_any(sent: str, names: List[str]) -> bool:
    for pat in compile_patterns(names):
        if pat.search(sent):
            return True
    return False
