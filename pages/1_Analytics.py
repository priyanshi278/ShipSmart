import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.markdown("""
<style>
/* File uploader label */
div[data-testid="stFileUploader"] label {
    color: white !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

# --- LOAD GLOBAL CSS ---
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.markdown("""<div class="sidebar-title"> <h4> 🚢 ShipSmart</h4>""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 class='page-title'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown("<p style='text-align: center; font-size:18px;'>✅ File uploaded successfully!</p>", unsafe_allow_html=True)

    # --- Summary Cards ---
    total_rows = df.shape[0]
    total_cols = df.shape[1]
    missing_vals = df.isnull().sum().sum()
    duplicate_vals = df.duplicated().sum()

    # Create 4 columns
    c1, c2, c3, c4 = st.columns(4)

    # Insert custom metric cards
    with c1:
        st.markdown(f"""
            <div class="metric-card blue">
                <h2>{total_rows:,}</h2>
                <p>Rows</p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card green">
                <h2>{total_cols}</h2>
                <p>Columns</p>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card orange">
                <h2>{missing_vals}</h2>
                <p>Missing Values</p>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card red">
                <h2>{duplicate_vals}</h2>
                <p>Duplicates</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📂 Available Analysis")

    # --- 1. Dataset Overview ---
    with st.expander("📌 Dataset Overview", expanded=False):
        st.markdown("🔹 Preview the dataset and check column information.")
        st.subheader("🔎 Dataset Preview")
        st.dataframe(df.head())

        st.subheader("📌 Dataset Information")
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(pd.DataFrame(df.dtypes, columns=["Type"]))

    # --- 2. Descriptive Statistics ---
    with st.expander("📊 Descriptive Statistics"):
        st.markdown("🔹 Summary statistics (mean, std, min, max, etc.) for numerical and categorical features.")
        st.dataframe(df.describe(include="all").transpose())


    # --- 4. Correlation Heatmap ---
    with st.expander("🔥 Correlation Heatmap"):
        st.markdown("🔹 Visualize correlations between numerical features.")
        numeric_df = df.select_dtypes(include=np.number)
        if not numeric_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.info("No numeric columns available for correlation heatmap.")

    # --- 5. Feature Distributions ---
    with st.expander("📈 Feature Distributions"):
        col1, col2 = st.columns([1.7, 2])  # Adjust width ratio if needed

        with col1:
            st.markdown("🔹 Explore the distribution of individual features.")
            st.markdown("👉 Select a feature to visualize")

        with col2:
            feature = st.selectbox("", df.columns, key="dist")
        fig = px.histogram(df, x=feature, nbins=30, title=f"Distribution of {feature}")
        st.plotly_chart(fig, use_container_width=True)

    # --- 7. Feature Comparison ---
    with st.expander("⚖️ Feature Comparison"):
        st.markdown("🔹 Compare two features using scatterplots, boxplots, or grouped histograms.")
            # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("Select X-axis feature")
            x_feature = st.selectbox("", df.columns, index=0, key="x")

        with col2:
            st.markdown("Select Y-axis feature")
            y_feature = st.selectbox("", df.columns, index=1, key="y")

        if pd.api.types.is_numeric_dtype(df[x_feature]) and pd.api.types.is_numeric_dtype(df[y_feature]):
            fig = px.scatter(df, x=x_feature, y=y_feature, trendline="ols",
                             title=f"{x_feature} vs {y_feature}")
            st.plotly_chart(fig, use_container_width=True)

        elif pd.api.types.is_object_dtype(df[x_feature]) and pd.api.types.is_numeric_dtype(df[y_feature]):
            fig = px.box(df, x=x_feature, y=y_feature,
                         title=f"{x_feature} vs {y_feature}")
            st.plotly_chart(fig, use_container_width=True)

        elif pd.api.types.is_object_dtype(df[x_feature]) and pd.api.types.is_object_dtype(df[y_feature]):
            fig = px.histogram(df, x=x_feature, color=y_feature, barmode="group",
                               title=f"{x_feature} vs {y_feature}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("⚠️ Unsupported feature type combination for comparison.")

else:
    st.markdown("<p style='text-align: center; font-size:18px;'>👆 Please upload a CSV file to start analysis</p>", unsafe_allow_html=True)
