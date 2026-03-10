import streamlit as st
import pandas as pd

from text_analysis import run_text_analysis
from Visualization import run_visualization

st.set_page_config(page_title="AI Data Assistant", layout="wide")

st.title("AI Data Analysis Assistant")

st.info(
    "Please upload your dataset in **CSV format (.csv)**. "
    "Excel files should be converted to CSV before uploading."
)

# Upload dataset

st.sidebar.header("Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload dataset (CSV format only)",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("No file uploaded yet. Upload a **.csv file** to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)

st.success("CSV file uploaded successfully")

with st.expander("Dataset Preview"):
    st.dataframe(df, use_container_width=True)

st.divider()

# Mode selection

mode = st.radio(
    "Choose how you want to interact with the data",
    ["Ask Question", "Generate Visualization", "Question with Visualization"],
    horizontal=True
)

st.divider()

# Layout

col1, col2, col3 = st.columns([1, 1, 2])

# Query input

with col1:

    st.subheader("Query Input")

    query = st.text_area(
        "Enter your query",
        height=180,
        placeholder="Example: Show sales trend over time"
    )

    submit = st.button("Submit Query")

# Query output

with col2:

    st.subheader("Query Output")

    text_output = st.empty()

# Visualization output

with col3:

    st.subheader("Visualization Output")

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
                    chart_output.pyplot(fig, use_container_width=True)

                except Exception as e:

                    chart_output.error("Visualization failed")
                    chart_output.write(str(e))

            # BOTH
            elif mode == "Question with Visualization":

                try:
                    result = run_text_analysis(df, query)

                    text_output.success("Analysis Completed")
                    text_output.write(result)

                except Exception as e:

                    text_output.error("Error in analysis")
                    text_output.write(str(e))

                try:
                    fig = run_visualization(df, query)

                    chart_output.success("Visualization Generated")
                    chart_output.pyplot(fig, use_container_width=True)

                except Exception as e:

                    chart_output.error("Visualization failed")
                    chart_output.write(str(e))