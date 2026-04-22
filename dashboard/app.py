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

# --- CACHE THE MODELS ---
# This ensures the 6GB Qwen model and RoBERTa don't reload on every button click!
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

# --- UI HEADER ---
st.title("🏛️ poli-stance")
st.markdown("**Explainable Political Ideology & Framing Analysis**")
st.divider()

# --- INPUT SECTION ---
st.subheader("1. Input Article")
default_text = "The administration unveiled its new economic plan today. Critics argue that the tax cuts disproportionately benefit large corporations while neglecting the working class. Supporters say the plan will spur job creation."
article_input = st.text_area("Paste the news article here:", value=default_text, height=150)
analyze_button = st.button("Run poli-stance Pipeline 🚀", type="primary")

st.divider()

# --- OUTPUT SECTION ---
if analyze_button and article_input.strip():
    with st.spinner('Running Preprocessing, Ideology Prediction, and Explanation Engine...'):
        
        # 1. Pipeline Execution
        ideo_result = ideology_model.predict(article_input)
        evidence = evidence_model.get_top_k_sentences(article_input, ideo_result, top_k=2)
        frame, frame_conf = framer.analyze(article_input)
        
        stance_output = run_stance_pipeline(
            text=article_input, clf=stance_clf, nlp=nlp,
            use_mock_registry=True, do_ner_target_suggestion=True, retrieval_mode="strict"
        )
        
        simplified_stances = {res["target"]: res["label"] for res in stance_output["all_results"] if res["label"] != "no_evidence"}

        state = {
            "raw_text": article_input,
            "ideology_label": ideo_result['ideology_label'],
            "confidence": ideo_result['confidence'],
            "evidence_sentences": evidence,
            "stances": simplified_stances, 
            "frame": frame
        }
        
        # 2. Generate Rationale
        raw_output = explainer.generate_rationale(state)
        try:
            clean_json_str = raw_output.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json_str)
        except:
            st.error("Failed to parse LLM Output. Raw text:")
            st.write(raw_output)
            st.stop()
            
    st.subheader("2. Analysis Results")
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### Source Text")
        st.info(article_input)
        st.markdown("**Detected Entity Stances:**")
        st.json(simplified_stances)
        
    with col2:
        st.markdown("#### Final Classification")
        color = "gray"
        if result["classification"] == "Left": color = "blue"
        elif result["classification"] == "Right": color = "red"
        elif result["classification"] == "Center": color = "violet"

        st.markdown(f"### :{color}[{result['classification']}]")
        st.write(f"**Rationale:** {result.get('rationale', 'N/A')}")
        
        with st.expander("🔍 View Explanation Engine Reasoning (Under the Hood)"):
            st.markdown("**Base Reasoning**")
            st.write(result.get('base_reasoning', 'N/A'))
            st.markdown("**Contrastive Logic**")
            st.write(result.get('contrastive_reasoning', 'N/A'))
            st.markdown("**Confidence Calibration**")
            st.write(result.get('confidence_note', 'N/A'))