# tests/test_target_extraction.py

from stance.registry import MOCK_TARGET_REGISTRY
from stance.target_extraction import (
    sentence_mentions_any,
    split_sentences,
    suggest_targets,
    suggest_targets_from_ner,
    suggest_targets_from_registry_issues,
)

# ---- tiny fake NLP layer ----


class FakeSpan:
    def __init__(self, text, label_=None):
        self.text = text
        self.label_ = label_


class FakeDoc:
    def __init__(self, sentences, ents):
        self._sents = [FakeSpan(s) for s in sentences]
        self.ents = ents

    @property
    def sents(self):
        return self._sents


class FakeNLP:
    def __init__(self, sentence_map, ent_map):
        self.sentence_map = sentence_map
        self.ent_map = ent_map

    def __call__(self, text):
        sentences = self.sentence_map.get(text, [text])
        ents = self.ent_map.get(text, [])
        return FakeDoc(sentences, ents)


def make_fake_nlp():
    text = (
        "Modi defended the bill. "
        "Congress criticized delimitation. "
        "The Women's Reservation Bill was discussed."
    )

    sentence_map = {
        text: [
            "Modi defended the bill.",
            "Congress criticized delimitation.",
            "The Women's Reservation Bill was discussed.",
        ]
    }

    ent_map = {
        text: [
            FakeSpan("Modi", "PERSON"),
            FakeSpan("Congress", "ORG"),
        ]
    }

    return FakeNLP(sentence_map, ent_map), text


def test_split_sentences():
    nlp, text = make_fake_nlp()
    sents = split_sentences(text, nlp)
    assert len(sents) == 3
    assert sents[0] == "Modi defended the bill."
    assert sents[1] == "Congress criticized delimitation."


def test_suggest_targets_from_ner_resolves_duplicates():
    nlp, text = make_fake_nlp()
    ents = suggest_targets_from_ner(text, nlp)
    assert ents == ["Modi", "Congress"]


def test_suggest_targets_from_registry_issues():
    text = "This article discusses delimitation and the Women's Reservation Bill."
    hits = suggest_targets_from_registry_issues(
        text,
        MOCK_TARGET_REGISTRY,
        country_filter="india",
    )
    assert "Delimitation" in hits
    assert "Women's Reservation Bill" in hits


def test_suggest_targets_combines_ner_and_issue_scan_and_resolves():
    nlp, text = make_fake_nlp()
    targets = suggest_targets(
        text=text,
        nlp=nlp,
        registry=MOCK_TARGET_REGISTRY,
        use_ner=True,
        use_issue_scan=True,
        country_filter="india",
    )
    assert "Narendra Modi" in targets  # resolved from "Modi"
    assert "Congress" in targets
    assert "Delimitation" in targets
    assert "Women's Reservation Bill" in targets


def test_sentence_mentions_any_alias():
    sent = "PM Modi said the reforms would help the economy."
    names = ["Narendra Modi", "Modi", "PM Modi"]
    assert sentence_mentions_any(sent, names) is True


def test_sentence_mentions_any_false():
    sent = "The chief minister addressed the crowd."
    names = ["Narendra Modi", "PM Modi"]
    assert sentence_mentions_any(sent, names) is False
