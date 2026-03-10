import streamlit as st
import pandas as pd
from text_analysis import run_text_analysis

st.set_page_config(page_title="AI Data Assistant", layout="wide")

st.title("AI Data Analysis Assistant")

st.info(
    "Please upload your dataset in **CSV format (.csv)**. "
    "Excel files should be converted to CSV before uploading."
)

# SIDEBAR UPLOAD


st.sidebar.header("Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload dataset (CSV format only)",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("No file uploaded yet. Upload a **.csv file** to continue.")
    st.stop()


# LOAD DATA


df = pd.read_csv(uploaded_file)

st.success("CSV file uploaded successfully")

with st.expander("Dataset Preview"):
    st.dataframe(df, use_container_width=True)

st.divider()


# MODE SELECTION


mode = st.radio(
    "Choose how you want to interact with the data",
    ["Ask Question", "Generate Visualization", "Question with Visualization"],
    horizontal=True
)

st.divider()

# -------------------------
# LAYOUT
# -------------------------

col1, col2, col3 = st.columns([1, 1, 1])


# QUERY INPUT


with col1:

    st.subheader("Query Input")

    query = st.text_area(
        "Enter your query",
        height=150,
        placeholder="Example: Which month has the highest sales?"
    )

    submit = st.button("Submit Query")

# -------------------------
# TEXT OUTPUT
# -------------------------

with col2:

    st.subheader("Query Output")

    text_output = st.empty()

# -------------------------
# VISUALIZATION OUTPUT
# -------------------------

with col3:

    st.subheader("Visualization Output")

    chart_output = st.empty()

# -------------------------
# RUN ANALYSIS
# -------------------------

if submit:

    if query.strip() == "":
        st.warning("Please enter a query.")
    else:

        with st.spinner("Analyzing dataset..."):

            try:
                result = run_text_analysis(df, query)

                text_output.success("Analysis Completed")
                text_output.write(result)

            except Exception as e:

                text_output.error("Error while processing query")
                text_output.write(str(e))