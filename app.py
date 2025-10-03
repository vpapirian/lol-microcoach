import streamlit as st
import pandas as pd
from microcoach.features import extract_features
from microcoach.compare import compare_to_baselines
from microcoach.advice import generate_advice

st.title("LoL MicroMotion Coach — MVP")

user_csv = st.file_uploader("Upload YOUR parsed movement CSV", type=["csv"])
pro_csvs = st.file_uploader("Upload PRO baseline CSV(s)", type=["csv"], accept_multiple_files=True)

if user_csv and pro_csvs:
    user_df = pd.read_csv(user_csv)
    user_feats = extract_features(user_df)

    pro_feats = []
    for f in pro_csvs:
        df = pd.read_csv(f)
        pro_feats.append((f.name, extract_features(df)))

    dists = compare_to_baselines(user_feats, pro_feats)
    st.subheader("Similarity to Baselines (lower = better)")
    st.table(pd.DataFrame(dists, columns=["baseline","distance"]))

    st.subheader("Your median features")
    st.write(user_feats.median(numeric_only=True))

    st.subheader("What to practice next")
    pro_all = pd.concat([pf for _,pf in pro_feats], ignore_index=True)
    tips = generate_advice(user_feats.median(numeric_only=True).to_dict(),
                           pro_all.median(numeric_only=True).to_dict())
    for t in tips:
        st.markdown(f"- {t}")
else:
    st.info("Upload one of your CSVs and at least one pro CSV to begin.")
