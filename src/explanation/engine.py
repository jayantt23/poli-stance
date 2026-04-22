import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

class ExplanationEngine:
    def __init__(self, model_id="Qwen/Qwen2.5-3B-Instruct"):
        self.model_id = model_id
        print(f"Loading Explanation Model from Hugging Face: {self.model_id}...")
        
        # Setup 4-bit Quantization for GPU efficiency
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        # Load directly from the Hugging Face hub
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            quantization_config=quantization_config
        )
        print("Engine Ready.")

    def _build_prompt(self, state):
        """Constructs the exact instruction for the LLM based on team data."""
        system_prompt = (
            "You are an expert political discourse analyst. Your job is to explain WHY a news "
            "article was classified as a specific ideology.\n\n"
            "Return the output as a clean JSON object strictly with these exact keys:\n"
            "- 'classification': The ideology label.\n"
            "- 'base_reasoning': Explain how the Frame, Stances, and Evidence support the label.\n"
            "- 'contrastive_reasoning': Explicitly state why the text does NOT align with the opposing ideology (or why it isn't an extreme if Center).\n"
            "- 'confidence_note': Analyze the exact confidence score (if < 0.80, explicitly acknowledge the ambiguity or moderation in the text).\n"
            "- 'rationale': A final 1-2 sentence summary combining the above.\n\n"
            "Important Guidelines:\n"
            "Disentanglement: Always distinguish between sentiment toward a person/entity and the underlying policy frame."
        )
        
        user_prompt = (
            f"Ideology Classification: {state['ideology_label']} (Confidence: {state['confidence']})\n"
            f"Dominant Frame: {state['frame']}\n"
            f"Entity Stances: {json.dumps(state['stances'])}\n"
            f"Top Evidence:\n- " + "\n- ".join(state['evidence_sentences']) + "\n\n"
            "Provide the JSON output."
        )

        # Use Qwen's specific chat template
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    def generate_rationale(self, state):
        """Runs the LLM and returns the explanation."""
        prompt = self._build_prompt(state)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        print("Generating rationale...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.3,     # Low temperature for analytical consistency
                do_sample=True
            )
        
        # Extract only the newly generated text
        input_length = inputs['input_ids'].shape[1]
        response = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
        
        return response

if __name__ == "__main__":
    # Test block
    mock_data = {
        "raw_text": "The new infrastructure bill passed with significant bipartisan compromises.",
        "ideology_label": "Center",
        "confidence": 0.78,
        "evidence_sentences": ["The new infrastructure bill passed with significant bipartisan compromises."],
        "stances": {"infrastructure bill": "Positive"},
        "frame": "Infrastructure & Bipartisanship"
    }
        
    engine = ExplanationEngine()
    result = engine.generate_rationale(mock_data)
    
    print("\n=== FINAL EXPLANATION ===")
    print(result)