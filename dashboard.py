import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="AI Trader Dashboard", layout="wide")
st.title("AI Trader - Trade Logg")

conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM trades ORDER BY time DESC", conn)
st.dataframe(df)
