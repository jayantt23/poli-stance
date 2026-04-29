import streamlit as st
import json
import sys
import os

# Ensure Python can find your 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.framing.analyzer import FramingAnalyzer
from src.ideology.predictor import IdeologyPredictor
from src.evidence.extractor import EvidenceExtractor
from src.explanation.engine import ExplanationEngine
from src.stance.model_cache import get_nlp, get_zero_shot_pipeline
from src.stance.stance_service import run_stance_pipeline

st.set_page_config(page_title="poli-stance", page_icon="🏛️", layout="wide")

# =========================
# LOAD MODELS (CACHED)
# =========================
@st.cache_resource
def load_all_models():
    explainer = ExplanationEngine()
    ideology_model = IdeologyPredictor()
    evidence_model = EvidenceExtractor()
    framer = FramingAnalyzer(device=0)
    nlp = get_nlp()
    stance_clf = get_zero_shot_pipeline(device=0)
    return explainer, ideology_model, evidence_model, framer, nlp, stance_clf

with st.spinner("Loading AI Models into GPU... (This takes 2-3 minutes)"):
    explainer, ideology_model, evidence_model, framer, nlp, stance_clf = load_all_models()

# =========================
# UI HEADER
# =========================
st.title("🏛️ poli-stance")
st.markdown("**Explainable Political Ideology & Framing Analysis**")
st.divider()

# =========================
# INPUT TEXT
# =========================
st.subheader("1. Input Article")

default_text = """The administration unveiled its new economic plan today. 
Critics argue that the tax cuts disproportionately benefit large corporations 
while neglecting the working class. Supporters say the plan will spur job creation."""

article_input = st.text_area(
    "Paste the news article here:",
    value=default_text,
    height=150
)

# =========================
# TARGET SELECTION
# =========================
st.subheader("2. What do you want to analyze?")

mode = st.radio(
    "Target selection mode:",
    ["Auto-detect targets", "Custom targets", "Both"],
    horizontal=True
)

custom_targets_input = st.text_input(
    "Enter targets (comma-separated):",
    placeholder="e.g. Trump, Harris, Biden, Gun violence.."
)

st.caption("Tip: Leave blank for auto-detection, or specify targets for focused analysis.")

analyze_button = st.button("Run poli-stance Pipeline 🚀", type="primary")

st.divider()


# =========================
# OUTPUT
# =========================
if analyze_button and article_input.strip():

    with st.spinner("Running full pipeline..."):

        # -------------------------
        # Parse user targets
        # -------------------------
        user_targets = None
        if mode in ["Custom targets", "Both"] and custom_targets_input.strip():
            user_targets = [
                t.strip() for t in custom_targets_input.split(",") if t.strip()
            ]

        # -------------------------
        # Ideology + Evidence + Frame
        # -------------------------
        ideo_result = ideology_model.predict(article_input)

        evidence = evidence_model.get_top_k_sentences(
            article_input, ideo_result, top_k=5
        )

        frame, frame_conf = framer.analyze(article_input)

        # -------------------------
        # Stance Pipeline
        # -------------------------
        stance_output = run_stance_pipeline(
            text=article_input,
            clf=stance_clf,
            nlp=nlp,
            targets=user_targets,
            use_mock_registry=True,
            do_ner_target_suggestion=(mode != "Custom targets"),
            retrieval_mode="strict"
        )

        # -------------------------
        # Simplified stance view
        # -------------------------
        simplified_stances = {
            res["target"]: res["label"]
            for res in stance_output["all_results"]
            if res["label"] != "no_evidence"
        }

        # -------------------------
        # Build state (intermediate)
        # -------------------------
        state = {
            "raw_text": article_input,
            "ideology_label": ideo_result["ideology_label"],
            "confidence": ideo_result["confidence"],
            "evidence_sentences": evidence,
            "stances": simplified_stances,
            "frame": frame
        }

        # -------------------------
        # Explanation Engine
        # -------------------------
        raw_output = explainer.generate_rationale(state)

        try:
            clean_json_str = raw_output.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json_str)
        except Exception:
            st.error("Failed to parse LLM Output. Raw text:")
            st.write(raw_output)
            st.stop()

        # =========================
        # FINAL PIPELINE OUTPUT
        # =========================
        final_output = {
            "input_text": article_input,
            "ideology": ideo_result,
            "framing": {
                "label": frame,
                "confidence": frame_conf
            },
            "stance": stance_output,
            "explanation": result
        }

    # =========================
    # DISPLAY RESULTS
    # =========================
    st.subheader("3. Analysis Results")

    col1, col2 = st.columns([1, 1.2])

    # ─────────────────────────
    # LEFT COLUMN
    # ─────────────────────────
    with col1:
        st.markdown("#### Source Text")
        st.info(article_input)

        # -------------------------
        # KEY EVIDENCE SENTENCES
        # -------------------------
        st.markdown("#### 🔑 Key Evidence Sentences")
        st.caption(
            f"Top {len(evidence)} sentence(s) most strongly driving the "
            f"**{ideo_result['ideology_label']}** classification:"
        )

        if evidence:
            label = ideo_result["ideology_label"]
            border_color = (
                "#e63946" if label == "Right"
                else "#457b9d" if label == "Left"
                else "#6c757d"
            )
            bg_color = (
                "rgba(230,57,70,0.07)" if label == "Right"
                else "rgba(69,123,157,0.07)" if label == "Left"
                else "rgba(108,117,125,0.07)"
            )

            for i, sent in enumerate(evidence, 1):
                st.markdown(
                    f"""
                    <div style="
                        background-color: {bg_color};
                        border-left: 4px solid {border_color};
                        border-radius: 6px;
                        padding: 10px 14px;
                        margin-bottom: 10px;
                        font-size: 0.95em;
                        line-height: 1.5;
                    ">
                        <span style="color:{border_color}; font-weight:700;">#{i}</span>
                        &nbsp; {sent}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No key sentences could be extracted.")

        # -------------------------
        # REQUESTED TARGETS
        # -------------------------
        st.markdown("### 🎯 Requested Targets")

        requested = stance_output["results_for_requested_targets"]

        if not requested:
            st.info("No requested targets provided or no evidence found.")
        else:
            for res in requested:
                if res["label"] == "no_evidence":
                    continue
                with st.expander(f"{res['target']} → {res['label']}"):
                    st.write("**Scores:**", res["scores"])
                    st.write("**Evidence:**")
                    for e in res["evidence"]:
                        st.write(f"- {e}")

        # -------------------------
        # FULL PIPELINE JSON
        # -------------------------
        st.markdown("### Full System Output")
        with st.expander("View full pipeline JSON"):
            st.json(final_output)

    # ─────────────────────────
    # RIGHT COLUMN
    # ─────────────────────────
    with col2:
        st.markdown("#### Final Classification")

        color = "gray"
        if result["classification"] == "Left":
            color = "blue"
        elif result["classification"] == "Right":
            color = "red"
        elif result["classification"] == "Center":
            color = "violet"

        st.markdown(f"### :{color}[{result['classification']}]")
        st.write(f"**Rationale:** {result.get('rationale', 'N/A')}")

        with st.expander("🔍 View Explanation Engine Reasoning"):
            st.markdown("**Base Reasoning**")
            st.write(result.get("base_reasoning", "N/A"))

            st.markdown("**Contrastive Logic**")
            st.write(result.get("contrastive_reasoning", "N/A"))

            st.markdown("**Confidence Calibration**")
            st.write(result.get("confidence_note", "N/A"))

        # -------------------------
        # CONFIDENCE BREAKDOWN
        # -------------------------
        st.markdown("#### 📊 Confidence Breakdown")

        probs = ideo_result.get("probs_full", {})
        if probs:
            label_colors = {"Right": "#e63946", "Center": "#6c757d", "Left": "#457b9d"}
            for lbl, prob in sorted(probs.items(), key=lambda x: -x[1]):
                bar_color = label_colors.get(lbl, "#888")
                pct = prob * 100
                st.markdown(
                    f"""
                    <div style="margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between;
                                    font-size:0.9em; margin-bottom:3px;">
                            <span><b>{lbl}</b></span>
                            <span>{pct:.1f}%</span>
                        </div>
                        <div style="background:#e0e0e0; border-radius:4px; height:10px;">
                            <div style="width:{pct}%; background:{bar_color};
                                        height:10px; border-radius:4px;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
