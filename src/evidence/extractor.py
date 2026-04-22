import re

class EvidenceExtractor:
    def __init__(self):
        # No heavy model to load here! It borrows the pipeline from the Predictor.
        print("Evidence Extractor initialized.")

    def get_top_k_sentences(self, text, ideology_result, top_k=2):
        """
        Scores individual sentences using the ideology pipeline to find 
        which ones most strongly support the document's predicted label.
        """
        predicted_label = ideology_result['ideology_label']
        classifier_pipeline = ideology_result['pipeline']
        
        # Split into sentences (keeping ones with meaningful length)
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s for s in sentences if len(s) > 20]

        if len(sentences) <= top_k:
            return sentences

        scored_sentences = []
        
        # Run the ideology model on each sentence individually
        for sent in sentences:
            raw_output = classifier_pipeline(sent)
            results = raw_output[0] if isinstance(raw_output[0], list) else raw_output
            probs = {res['label']: res['score'] for res in results}
            
            # How strongly does this sentence support the OVERALL document label?
            target_confidence = probs.get(predicted_label, 0.0)
            
            scored_sentences.append({
                'sentence': sent,
                'confidence_for_target': target_confidence
            })

        # Sort by the highest confidence for the predicted label
        scored_sentences.sort(key=lambda x: x['confidence_for_target'], reverse=True)
        
        return [item['sentence'] for item in scored_sentences[:top_k]]