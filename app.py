import streamlit as st
import pandas as pd

from text_analysis import run_text_analysis
from Visualization import run_visualization

st.set_page_config(
    page_title="AI Data Assistant",
    layout="wide",
    page_icon="📊"
)

# Header
st.markdown(
    """
    <h1 style='text-align:center;'>AI Data Analysis Assistant</h1>
    <p style='text-align:center; font-size:18px; color:gray;'>
    Upload your dataset and interact with it using natural language
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# Sidebar upload
st.sidebar.header("📁 Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload dataset (CSV format only)",
    type=["csv"]
)

st.sidebar.info(
    "Supported Format: CSV\n\n"
    "Convert Excel files to CSV before uploading."
)

if uploaded_file is None:
    st.warning("Upload a **CSV dataset** from the sidebar to begin.")
    st.stop()

df = pd.read_csv(uploaded_file)

st.success("Dataset uploaded successfully")

# Dataset preview
with st.expander("📄 Preview Dataset", expanded=False):
    st.dataframe(df, width="stretch")

st.divider()

# Mode selection
st.markdown("### Interaction Mode")

mode = st.radio(
    "",
    ["Ask Question", "Generate Visualization"],
    horizontal=True
)

st.divider()

# Layout columns
col1, col2, col3 = st.columns([1.1, 1.2, 2])

# Query input
with col1:

    st.markdown("### ✏ Query Input")

    query = st.text_area(
        "Enter your query",
        height=200,
        placeholder="Example:\n• What is the average sales value?\n• Show sales trend over time\n• Compare category sales"
    )

    submit = st.button("🚀 Run Analysis", use_container_width=True)

# Query output
with col2:

    st.markdown("### 📑 Analysis Result")

    output_box = st.container(border=True)

    with output_box:
        text_output = st.empty()

# Visualization output
with col3:

    st.markdown("### 📊 Visualization")

    chart_box = st.container(border=True)

    with chart_box:
        chart_output = st.empty()

# Run analysis
if submit:

    if query.strip() == "":
        st.warning("Please enter a query")

    else:

        with st.spinner("Analyzing dataset..."):

            # TEXT ONLY
            if mode == "Ask Question":

                try:
                    result = run_text_analysis(df, query)

                    text_output.success("Analysis Completed")
                    text_output.write(result)

                except Exception as e:

                    text_output.error("Error while processing query")
                    text_output.write(str(e))

            # VISUALIZATION ONLY
            elif mode == "Generate Visualization":

                try:
                    fig = run_visualization(df, query)

                    chart_output.success("Visualization Generated")
                    chart_output.pyplot(fig, width="stretch")

                except Exception as e:

                    chart_output.error("Visualization failed")
                    chart_output.write(str(e))