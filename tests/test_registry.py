# tests/test_registry.py

from stance.registry import (
    MOCK_TARGET_REGISTRY,
    TARGET_REGISTRY,
    get_aliases,
    get_related,
    resolve_target,
)


def test_resolve_target_exact_canonical():
    assert resolve_target("Narendra Modi", MOCK_TARGET_REGISTRY) == "Narendra Modi"


def test_resolve_target_alias():
    assert resolve_target("Modi", MOCK_TARGET_REGISTRY) == "Narendra Modi"
    # CORRECT – the canonical key is what gets returned
    assert resolve_target("YSR Congress", TARGET_REGISTRY) == "YSR Congress"

    # CORRECT – an alias resolves to the canonical key
    assert resolve_target("Jagan party", TARGET_REGISTRY) == "YSR Congress"
    assert resolve_target("Didi", MOCK_TARGET_REGISTRY) == "Mamata Banerjee"
    assert resolve_target("GOP", MOCK_TARGET_REGISTRY) == "Republican Party"


def test_resolve_target_unknown_falls_back():
    assert resolve_target("Tejashwi Yadav", MOCK_TARGET_REGISTRY) == "Tejashwi Yadav"


def test_get_aliases_includes_canonical_and_aliases():
    aliases = get_aliases(MOCK_TARGET_REGISTRY, "Narendra Modi")
    assert "Narendra Modi" in aliases
    assert "Modi" in aliases
    assert "PM Modi" in aliases


def test_get_aliases_unknown_returns_canonical_only():
    aliases = get_aliases(MOCK_TARGET_REGISTRY, "Some Unknown Target")
    assert aliases == ["Some Unknown Target"]


def test_get_related():
    related = get_related(MOCK_TARGET_REGISTRY, "Narendra Modi")
    assert "BJP" in related
