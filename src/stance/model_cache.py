from functools import lru_cache

import spacy
from transformers import pipeline


@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load("en_core_web_sm")


@lru_cache(maxsize=1)
def get_zero_shot_pipeline(
    model_name: str = "facebook/bart-large-mnli", device: int = -1
):
    return pipeline("zero-shot-classification", model=model_name, device=device)


# do this every where else
# from stance.model_cache import get_nlp, get_zero_shot_pipeline

# nlp = get_nlp()
# clf = get_zero_shot_pipeline()


# import streamlit as st
# from transformers import pipeline
# import spacy

# @st.cache_resource
# def get_nlp():
#     return spacy.load("en_core_web_sm")

# @st.cache_resource
# def get_zero_shot_pipeline():
#     return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1)
