import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="ShipSmart", page_icon="🚢", layout="wide")

# --- LOAD GLOBAL CSS ---
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.sidebar.markdown("""<div class="sidebar-title"> <h4> 🚢 ShipSmart</h4>""", unsafe_allow_html=True)
# --- TITLE ---
st.markdown("""
<div class="intro">
    <h1>🚢 Welcome to ShipSmart</h1>
    <p>ShipSmart is a modern interactive dashboard for analyzing ship performance and operational efficiency. Perform exploratory data analysis to uncover trends and patterns, and use clustering analysis to segment ships based on key metrics and categorical attributes for actionable insights.</p>
</div>
""", unsafe_allow_html=True)


# --- Why Choose ShipSmart Section ---
st.markdown("### 🌟 Why Choose ShipSmart?")
st.write("")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h4>📂 Upload & Explore</h4>
        <p>Quickly upload your ship and voyage datasets to inspect your data. Preview rows, view column details, and access descriptive statistics in one interactive dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h4>📊 Interactive Comparisons</h4>
        <p>Compare ships across speed, cargo load, draft, and turnaround time using dynamic charts and graphs. Identify trends and performance differences across vessels and routes.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h4> 🤖 Ship Performance Clustering</h4>
        <p>Automatically group ships into High, Medium, or Low efficiency clusters based on operational metrics. Explore cluster distributions to understand variations across your fleet.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h4>📈 Data Exploration</h4>
        <p>Perform EDA with descriptive statistics, correlation heatmaps, and feature distributions to uncover patterns, trends, and insights across ships and voyages interactively.</p>
    </div>
    """, unsafe_allow_html=True)

