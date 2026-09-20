# CSE 594 Human AI Interaction Assignment1-2
Emotion Labeling

Streamlit web interface for labeling "tweets" dataset with basic emotions.

## Setup
pip install -r requirements.txt
streamlit run app.py

## Files
- `app.py` — Streamlit interface
- `prepare_data.py` — script to regenerate tweet pool from HuggingFace
- `tweets.csv` — 60 balanced tweets from dair-ai/emotion (test split)
- `labels.csv` — generated on submission, records participant labels