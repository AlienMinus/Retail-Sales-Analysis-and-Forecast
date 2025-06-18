import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📈 Walmart Sales Data Dashboard")

# Load dataset
@st.cache_data

def load_data():
    df = pd.read_csv("df_sql.csv")
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    df.sort_values("Date", inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
store_options = st.sidebar.multiselect("Select Store(s)", options=df["Store"].unique(), default=df["Store"].unique())
dept_options = st.sidebar.multiselect("Select Department(s)", options=df["Dept"].unique(), default=df["Dept"].unique())
holiday_filter = st.sidebar.selectbox("Holiday Filter", ["All", "Holiday Weeks", "Non-Holiday Weeks"])

# Filter data
filtered_df = df[df["Store"].isin(store_options) & df["Dept"].isin(dept_options)]
if holiday_filter == "Holiday Weeks":
    filtered_df = filtered_df[filtered_df["IsHoliday"] == 1]
elif holiday_filter == "Non-Holiday Weeks":
    filtered_df = filtered_df[filtered_df["IsHoliday"] == 0]

# KPIs
st.subheader("📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Weekly_Sales'].sum():,.2f}")
col2.metric("Average Weekly Sales", f"${filtered_df['Weekly_Sales'].mean():,.2f}")
col3.metric("Total Records", f"{filtered_df.shape[0]:,}")

# Time Series Line Chart
st.subheader("📅 Weekly Sales Trend")
time_series = filtered_df.groupby("Date")["Weekly_Sales"].sum().reset_index()
fig_line = px.line(time_series, x="Date", y="Weekly_Sales", title="Total Weekly Sales Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# Sales by Store
st.subheader("🏪 Sales by Store")
sales_by_store = filtered_df.groupby("Store")["Weekly_Sales"].sum().sort_values(ascending=False)
fig_store = px.bar(sales_by_store, x=sales_by_store.index, y=sales_by_store.values, labels={"x": "Store", "y": "Total Sales"})
st.plotly_chart(fig_store, use_container_width=True)

# Boxplot: Sales by Store Type
st.subheader("📦 Sales Distribution by Store Type")
fig_box, ax = plt.subplots()
sns.boxplot(data=filtered_df, x="Type", y="Weekly_Sales", ax=ax)
st.pyplot(fig_box)

# Correlation Heatmap
st.subheader("🔍 Correlation Analysis")
numeric_cols = ["Weekly_Sales", "Temperature", "Fuel_Price", "CPI", "Unemployment", "Size", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
corr = filtered_df[numeric_cols].corr()
fig_corr, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig_corr)

st.markdown("---")
st.markdown("Made with ❤️ by [AlienMinus]")
