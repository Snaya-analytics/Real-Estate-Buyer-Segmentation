import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

# Load cleaned dataset
df = pd.read_csv("buyers_final.csv")

st.title("🏢 Real Estate Buyer Segmentation Dashboard")

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Buyers", len(df))
col2.metric("Avg Sale Price", f"${df['sale_price'].mean():,.0f}")
col3.metric("Avg Satisfaction", round(df['satisfaction_score'].mean(),2))
loan_pct = (df['loan_applied'].value_counts(normalize=True).get("Yes",0)*100)
col4.metric("Loan Applied %", f"{loan_pct:.1f}%")

# ---------------- Cluster Profiling Heatmap ----------------
st.header("📊 Cluster Profiling Heatmap")
numeric_cols = ['sale_price','floor_area_sqft','satisfaction_score']
profiling = df.groupby('client_type')[numeric_cols].mean().round(2)
fig1, ax1 = plt.subplots()
sns.heatmap(profiling, annot=True, cmap="coolwarm", ax=ax1)
st.pyplot(fig1)

# ---------------- Loan Behavior Bar Chart ----------------
st.header("💳 Loan Behavior Bar Chart")
loan_chart = df.groupby(['client_type','loan_applied']).size().reset_index(name='count')
fig2, ax2 = plt.subplots()
sns.barplot(x="client_type", y="count", hue="loan_applied", data=loan_chart, palette="Paired", ax=ax2)
st.pyplot(fig2)

# ---------------- Satisfaction Score Trend ----------------
st.header("📈 Satisfaction Score Trend")
trend = df.groupby('transaction_date')['satisfaction_score'].mean()
st.line_chart(trend)

# ---------------- Acquisition Purpose Pie Chart ----------------
st.header("🥧 Acquisition Purpose Pie Chart")
purpose_counts = df['acquisition_purpose'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(purpose_counts, labels=purpose_counts.index, autopct='%1.1f%%')
st.pyplot(fig3)

# ---------------- Sale Price Boxplot ----------------
st.header("💰 Sale Price Boxplot")
fig4, ax4 = plt.subplots()
sns.boxplot(x="client_type", y="sale_price", data=df, palette="Set3", ax=ax4)
st.pyplot(fig4)

# ---------------- Geographic Buyer Analysis ----------------
st.header("🗺️ Geographic Buyer Analysis")
if "longitude" in df.columns and "latitude" in df.columns:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=20, longitude=78, zoom=3),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color=[0, 128, 255, 160],
                get_radius=200,
            ),
        ],
    ))
else:
    st.warning("⚠️ No geographic columns found.")