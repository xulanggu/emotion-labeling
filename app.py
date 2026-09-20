# app.py
import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime


N_TWEETS_PER_SESSION = 5
EMOTIONS = ["anger", "fear", "joy", "love", "sadness", "surprise"]
LOG_PATH = "labels.csv"
TWEETS_PATH = "tweets.csv"

st.set_page_config(page_title="Tweet Emotion Labeling", page_icon="🏷️")

@st.cache_data
def load_pool():
    return pd.read_csv(TWEETS_PATH)

pool = load_pool()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
    st.session_state.stage = "consent"
    st.session_state.sample = None
    st.session_state.idx = 0
    st.session_state.labels = []
    st.session_state.participant = ""

if st.session_state.stage == "consent":
    st.title("🏷️ Tweet Emotion Labeling")
    st.markdown("""
    ### What you will do
    You will read **5 randomly selected tweets** data and label each with the
    emotion it most strongly expresses. Choose one from the 6 emotions below:

    **anger · fear · joy · love · sadness · surprise**

    ### Instructions
    - Please read the full tweet before deciding.
    - If two feel equally plausible, go with the stronger one.

    ### Data collected in this session
    Please notice that your name, the tweets you saw, your labels, and timestamps will be
    saved for CSE 594 A1-2 class assignment.
    """)
    name = st.text_input("Your name:")
    if st.button("Start", disabled=(not name.strip())):
        st.session_state.participant = name.strip()
        st.session_state.sample = pool.sample(
            n=N_TWEETS_PER_SESSION).reset_index(drop=True)
        st.session_state.stage = "labeling"
        st.rerun()

elif st.session_state.stage == "labeling":
    i = st.session_state.idx
    total = N_TWEETS_PER_SESSION
    st.progress(i / total, text=f"Tweet {i+1} of {total}")

    row = st.session_state.sample.iloc[i]
    st.markdown(f"### Tweet {i+1}")
    st.info(row["text"])

    choice = st.radio(
        "Which emotion does this tweet express?",
        EMOTIONS,
        index=None,
        key=f"radio_{i}",
    )

    if st.button("Next", disabled=(choice is None)):
        st.session_state.labels.append({
            "session_id": st.session_state.session_id,
            "participant": st.session_state.participant,
            "tweet_id": int(row["tweet_id"]),
            "tweet_text": row["text"],
            "true_label": row["emotion_name"],
            "user_label": choice,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })
        st.session_state.idx += 1
        if st.session_state.idx >= total:
            st.session_state.stage = "done"
        st.rerun()

elif st.session_state.stage == "done":
    df_new = pd.DataFrame(st.session_state.labels)
    header = not os.path.exists(LOG_PATH)
    df_new.to_csv(LOG_PATH, mode="a", header=header, index=False)

    st.success("✅ Thanks, your labels have been recorded!")
    st.markdown(f"**Session ID:** `{st.session_state.session_id}`")
    st.markdown("### Your labels:")
    st.dataframe(df_new[["tweet_text", "user_label", "true_label"]],
                 use_container_width=True)
    if st.button("Restart (new session)"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()