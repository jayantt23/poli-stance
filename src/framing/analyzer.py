from transformers import pipeline

class FramingAnalyzer:
    def __init__(self, device=0):
        print("Loading Framing Model (BART Zero-Shot)...")
        # device=0 loads it to the GPU
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=device 
        )
        self.frames = [
            "Economy & Class Conflict",
            "Economic Freedom & Free Market",
            "National Security & Sovereignty",
            "Governance & Corruption",
            "Public Welfare & Healthcare",
            "Infrastructure & Development",
            "Climate & Environment",
            "Identity & Social Justice",
            "Law & Order",
            "Foreign Policy & Diplomacy"
        ]

    def analyze(self, text):
        """Returns the top frame and its confidence score."""
        result = self.classifier(text, candidate_labels=self.frames)
        top_frame = result["labels"][0]
        confidence = float(result["scores"][0])
        
        return top_frame, round(confidence, 2)