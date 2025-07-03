import streamlit as st
import pandas as pd
import plotly.express as px
import io
from utils.relationship_detector import detect_relationships
from utils.chart_generator import generate_chart_options, create_chart

st.set_page_config(layout="wide", page_title="Power BI-style Auto Dashboard")

st.title("📊 Power BI-style Multi-File Dashboard Generator")

uploaded_files = st.file_uploader(
    "Upload multiple CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    dataframes = {}

    # Step 1: Load files
    for file in uploaded_files:
        filename = file.name
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        dataframes[filename] = df
        st.success(f"Loaded `{filename}`: {df.shape[0]} rows")

    # Step 2: Detect relationships
    st.subheader("🔗 Detected Relationships (PK/FK)")
    relations = detect_relationships(dataframes)

    if relations:
        for rel in relations:
            st.markdown(f"✅ `{rel[0]}.{rel[1]}` ↔ `{rel[2]}.{rel[3]}`")
    else:
        st.warning("No obvious relationships found. Using first table only.")

    # Step 3: Auto-join tables
    if relations:
        first = relations[0]
        df_joined = pd.merge(
            dataframes[first[0]],
            dataframes[first[2]],
            left_on=first[1],
            right_on=first[3],
            how="left"
        )
    else:
        df_joined = list(dataframes.values())[0]

    st.subheader("📄 Merged Data Preview")
    st.dataframe(df_joined.head())

    st.markdown("---")
    st.subheader("📊 Dynamic Chart Builder")

    chart_type = st.selectbox("Select Chart Type", generate_chart_options(df_joined))
    x_axis = st.selectbox("X-Axis", df_joined.columns)
    y_axis = st.selectbox("Y-Axis (if applicable)", ["None"] + list(df_joined.select_dtypes(include='number').columns))
    color = st.selectbox("Color (optional)", ["None"] + list(df_joined.columns))

    if st.button("📌 Add to Dashboard"):
        if "charts" not in st.session_state:
            st.session_state.charts = []
        st.session_state.charts.append({
            "type": chart_type,
            "x": x_axis,
            "y": y_axis if y_axis != "None" else None,
            "color": color if color != "None" else None
        })

    if "charts" in st.session_state and st.session_state.charts:
        st.subheader("📋 Your Dashboard")
        cols = st.columns(2)
        for i, config in enumerate(st.session_state.charts):
            fig = create_chart(df_joined, config)
            with cols[i % 2]:
                st.plotly_chart(fig, use_container_width=True)
