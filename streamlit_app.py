import pandas as pd
import streamlit as st
from pathlib import Path

st.title("LLM Bias Explorer (Task 08)")
sum_path = Path("analysis/summary_by_condition.csv")
if not sum_path.exists():
    st.warning("Run analyze_bias.py to generate summary_by_condition.csv")
else:
    df = pd.read_csv(sum_path)
    st.subheader("Summary by Condition")
    st.dataframe(df)

    st.bar_chart(df.set_index(["prompt_family","condition"])["vader_mean"])
    st.bar_chart(df.set_index(["prompt_family","condition"])["tb_mean"])
