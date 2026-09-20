
from datasets import load_dataset
import pandas as pd

EMOTIONS = ["sadness", "joy", "love", "anger", "fear", "surprise"]


PER_CLASS = 10  
SEED = 42


ds = load_dataset("dair-ai/emotion", "split", split="test")
df = pd.DataFrame(ds)
print(f"Loaded {len(df)} tweets from test split")
print(df["label"].value_counts().sort_index())


sampled = (df.groupby("label", group_keys=False)
             .apply(lambda x: x.sample(n=PER_CLASS, random_state=SEED)))


sampled = sampled.reset_index(drop=True)
sampled["tweet_id"] = sampled.index
sampled["emotion_name"] = sampled["label"].map(lambda i: EMOTIONS[i])


sampled = sampled[["tweet_id", "text", "label", "emotion_name"]]
sampled.to_csv("tweets.csv", index=False)
print(f"\nSaved {len(sampled)} tweets to tweets.csv")
print("\nFirst few rows:")
print(sampled.head())