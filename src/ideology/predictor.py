from transformers import pipeline
import torch

class IdeologyPredictor:
    def __init__(self, model_id="vriddhi-07/ideology_predictor_roberta"):
        print(f"Loading Ideology Model '{model_id}'...")
        
        # Use GPU if available
        device = 0 if torch.cuda.is_available() else -1
        
        self.classifier = pipeline(
            "text-classification",
            model=model_id,
            tokenizer=model_id,
            top_k=None,
            truncation=True,
            max_length=512,
            device=device
        )

    def predict(self, text):
        """Returns the predicted label, confidence, and the pipeline object."""
        if not text.strip():
            return {"ideology_label": "Center", "confidence": 0.0, "pipeline": self.classifier}

        raw_output = self.classifier(text)
        results = raw_output[0] if isinstance(raw_output[0], list) else raw_output
        
        probs = {res['label']: round(res['score'], 4) for res in results}
        best_label = max(probs, key=probs.get)

        return {
            "ideology_label": best_label,
            "confidence": probs[best_label],
            "probs_full": probs,
            "pipeline": self.classifier # Pass this to the Evidence Extractor!
        }