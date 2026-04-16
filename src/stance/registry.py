from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

# Minimal mock registry. Replace/extend this with your researched registry.
MOCK_TARGET_REGISTRY: Dict[str, Dict[str, Any]] = {
    # India
    "Narendra Modi": {
        "aliases": ["Narendra Modi", "Modi", "PM Modi", "Prime Minister Modi"],
        "related": ["BJP"],
        "kind": "person",
        "country": "india",
    },
    "Rahul Gandhi": {
        "aliases": ["Rahul Gandhi", "Rahul"],
        "related": ["Congress"],
        "kind": "person",
        "country": "india",
    },
    "Mamata Banerjee": {
        "aliases": ["Mamata Banerjee", "Mamata", "Didi", "CM Mamata"],
        "related": ["TMC"],
        "kind": "person",
        "country": "india",
    },
    "Amit Shah": {
        "aliases": ["Amit Shah", "Shah", "Home Minister Amit Shah"],
        "related": ["BJP"],
        "kind": "person",
        "country": "india",
    },
    "BJP": {
        "aliases": ["BJP", "Bharatiya Janata Party"],
        "related": ["Narendra Modi", "Amit Shah"],
        "kind": "party",
        "country": "india",
    },
    "Congress": {
        "aliases": ["Congress", "INC", "Indian National Congress"],
        "related": ["Rahul Gandhi", "Mallikarjun Kharge"],
        "kind": "party",
        "country": "india",
    },
    "TMC": {
        "aliases": [
            "TMC",
            "Trinamool",
            "Trinamool Congress",
            "All India Trinamool Congress",
        ],
        "related": ["Mamata Banerjee"],
        "kind": "party",
        "country": "india",
    },
    "AAP": {
        "aliases": ["AAP", "Aam Aadmi Party"],
        "related": ["Arvind Kejriwal"],
        "kind": "party",
        "country": "india",
    },
    "Arvind Kejriwal": {
        "aliases": ["Arvind Kejriwal", "Kejriwal"],
        "related": ["AAP"],
        "kind": "person",
        "country": "india",
    },
    "Mallikarjun Kharge": {
        "aliases": ["Mallikarjun Kharge", "Kharge"],
        "related": ["Congress"],
        "kind": "person",
        "country": "india",
    },
    "Demonetisation": {
        "aliases": [
            "Demonetisation",
            "demonetization",
            "demonetised",
            "demonetized",
            "notebandi",
        ],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Delimitation": {
        "aliases": ["Delimitation", "delimitation"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Women's Reservation Bill": {
        "aliases": [
            "Women's Reservation Bill",
            "women's reservation bill",
            "women's quota",
            "women quota",
            "33 per cent reservation",
            "33% reservation",
        ],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "CAA": {
        "aliases": ["CAA", "Citizenship Amendment Act", "Citizenship (Amendment) Act"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    "Farm Laws": {
        "aliases": ["Farm Laws", "farm laws", "three farm laws"],
        "related": [],
        "kind": "issue",
        "country": "india",
    },
    # US
    "Donald Trump": {
        "aliases": ["Donald Trump", "Trump", "President Trump"],
        "related": ["Republican Party"],
        "kind": "person",
        "country": "us",
    },
    "Joe Biden": {
        "aliases": ["Joe Biden", "Biden", "President Biden"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Bernie Sanders": {
        "aliases": ["Bernie Sanders", "Bernie", "Sanders"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Kamala Harris": {
        "aliases": ["Kamala Harris", "Kamala", "Vice President Harris"],
        "related": ["Democratic Party"],
        "kind": "person",
        "country": "us",
    },
    "Republican Party": {
        "aliases": ["Republican Party", "Republicans", "GOP"],
        "related": ["Donald Trump"],
        "kind": "party",
        "country": "us",
    },
    "Democratic Party": {
        "aliases": ["Democratic Party", "Democrats", "Dems"],
        "related": ["Joe Biden", "Bernie Sanders", "Kamala Harris"],
        "kind": "party",
        "country": "us",
    },
}


def load_registry_from_json(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_entry(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> Dict[str, Any]:
    return registry.get(canonical_target, {})


def get_aliases(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> List[str]:
    entry = get_entry(registry, canonical_target)
    aliases = entry.get("aliases", [])
    vals = [canonical_target] + aliases
    seen = set()
    out = []
    for x in vals:
        xl = x.lower()
        if xl not in seen:
            seen.add(xl)
            out.append(x)
    return out


def get_related(
    registry: Dict[str, Dict[str, Any]], canonical_target: str
) -> List[str]:
    entry = get_entry(registry, canonical_target)
    return entry.get("related", [])


def resolve_target(
    raw_target: str, registry: Optional[Dict[str, Dict[str, Any]]] = None
) -> str:
    """
    Map a raw target like 'Modi' or 'Didi' to the canonical key if found.
    Falls back to the raw target unchanged.
    """
    if registry is None:
        return raw_target

    if raw_target in registry:
        return raw_target

    raw_low = raw_target.strip().lower()
    for canonical, meta in registry.items():
        if raw_low == canonical.lower():
            return canonical
        for alias in meta.get("aliases", []):
            if raw_low == alias.lower():
                return canonical

    return raw_target
