
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Qahwa Corner Dashboard",
    page_icon="☕",
    layout="wide"
)

st.title("Qahwa Corner Sales Dashboard")
st.caption("Sales Data | January - June 2026")

@st.cache_data
def load_data():
    path = Path(__file__).parent / "cafe_sales.csv"
    return pd.read_csv(path)

df = load_data()

branches = sorted(df["branch"].dropna().unique())

selected_branch = st.selectbox(
    "Select a Branch",
    ["All branches"] + branches
)

if selected_branch == "All branches":
    data = df
else:
    data = df[df["branch"] == selected_branch]

total_revenue = data["total_sar"].sum()

st.metric(
    "Total Revenue (SAR)",
    f"{total_revenue:,.0f}"
)

st.subheader("Revenue by Product")

product_revenue = (
    data.groupby("product")["total_sar"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_revenue)

st.subheader("Monthly Revenue")

data = data.copy()
data["date"] = pd.to_datetime(data["date"])
data["month"] = data["date"].dt.to_period("M").astype(str)

monthly = data.groupby("month")["total_sar"].sum()

st.line_chart(monthly)

