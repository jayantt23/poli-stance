import streamlit as st
import json
import time

# Set up the page
st.set_page_config(page_title="poli-stance", page_icon="🏛️", layout="wide")

# In the final version, this will be generated dynamically by your NLP pipeline
mock_json_string = """
{
  "classification": "Center",
  "base_reasoning": "The text supports a center-left stance by emphasizing bipartisanship and infrastructure funding, which are common themes among center candidates.",
  "contrastive_reasoning": "This text does not strongly align with either the far-left or far-right extremes. It avoids endorsing extreme positions on taxes or climate change.",
  "confidence_note": "The text's moderate stance and balanced approach to various issues provide strong evidence for its center classification.",
  "rationale": "The text presents a center-left perspective by highlighting bipartisan compromise and infrastructure funding, while maintaining a balanced view on contentious issues, thus firmly placing it within the center ideological spectrum."
}
"""
result = json.loads(mock_json_string)

# --- UI HEADER ---
st.title("🏛️ poli-stance")
st.markdown("**Explainable Political Ideology & Framing Analysis**")
st.divider()

# --- INPUT SECTION ---
st.subheader("1. Input Article")
default_text = "The new infrastructure bill passed with significant bipartisan compromises. While it doesn't offer the sweeping climate reforms some activists wanted, it provides essential funding for repairing bridges and roads without drastically raising taxes on the middle class."

article_input = st.text_area("Paste the news article or transcript here:", value=default_text, height=150)
analyze_button = st.button("Run poli-stance Pipeline 🚀", type="primary")

st.divider()

# --- OUTPUT SECTION ---
# Only show the results if the button is clicked
if analyze_button:
    with st.spinner('Running Preprocessing, Ideology Prediction, and Explanation Engine...'):
        time.sleep(1.5) # Fake loading time to simulate the models running
        
    st.subheader("2. Analysis Results")
    
    # Create two columns to show the Article and the Results side-by-side
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### Source Text")
        # Put the article in a nice bordered box
        st.info(article_input)
        
    with col2:
        st.markdown("#### Final Classification")
        
        # Color code the output (Streamlit uses 'violet' instead of 'purple')
        color = "gray"
        if result["classification"] == "Left": color = "blue"
        elif result["classification"] == "Right": color = "red"
        elif result["classification"] == "Center": color = "violet"

        # The Streamlit markdown syntax for color is :{color}[text]
        st.markdown(f"### :{color}[{result['classification']}]")
        st.write(f"**Rationale:** {result['rationale']}")
        
        st.write("") # Spacer
        
        # The Developer Expander
        with st.expander("🔍 View Explanation Engine Reasoning (Under the Hood)"):
            st.markdown("**Base Reasoning**")
            st.write(result['base_reasoning'])
            
            st.markdown("**Contrastive Logic**")
            st.write(result['contrastive_reasoning'])
            
            st.markdown("**Confidence Calibration**")
            st.write(result['confidence_note'])