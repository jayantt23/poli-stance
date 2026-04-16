from transformers import pipeline

MODEL_ID = "vriddhi-07/ideology_predictor_roberta" 
print(f"Loading '{MODEL_ID}' from Hugging Face...")

ideology_clf = pipeline(
    "text-classification",
    model=MODEL_ID,
    tokenizer=MODEL_ID,
    top_k=None,
    truncation=True,
    max_length=512
)
print("Ideology Predictor module ready!\n")

def process_ideology(state):
    """
    Ingests the sequential state object, adds the document-level 
    ideology predictions, and returns the updated object.
    """

    text = state.get("raw_text", "").strip()
    if not text:
        return state
        
    raw_output = ideology_clf(text)  #get predictions from the model
    
    results = raw_output[0] if isinstance(raw_output[0], list) else raw_output
    probs = {res['label']: round(res['score'], 4) for res in results}
    best_label = max(probs, key=probs.get)

    state["ideology_pred"] = best_label
    state["ideology_confidence"] = probs[best_label]
    state["ideology_probs_full"] = probs
    
    return state

#sample main for testing
'''if __name__ == "__main__":
    import json
    
    #sample input
    mock_pipeline_state = {
        "raw_text": "The administration unveiled its new economic plan today. Critics argue that the tax cuts disproportionately benefit corporations. Supporters say the plan will spur job creation.",
        "sentences": [
            "The administration unveiled its new economic plan today.",
            "Critics argue that the tax cuts disproportionately benefit corporations.",
            "Supporters say the plan will spur job creation."
        ],
        "entities": [{"text": "administration", "label": "ORG"}]
    }

    print("Running integration test...")
    final_state = process_ideology(mock_pipeline_state)
    print(json.dumps(final_state, indent=2))'''