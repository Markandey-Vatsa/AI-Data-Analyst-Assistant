# AI Data Analyst Assistant

## Overview

**AI Data Analyst Assistant** is an intelligent data exploration tool that allows users to interact with their datasets using natural language. Instead of writing complex code or SQL queries, users can simply ask questions about their data and receive results instantly.

The application uses **Large Language Models (LLMs)** along with a **Python execution environment** to analyze datasets, generate insights, and create visualizations.

This project is designed to make **data analysis accessible to non-technical users** while also speeding up workflows for analysts and developers.

---

## Features

### 1. Talk to Your Data (Text Analysis)

Users can ask questions about their dataset in natural language.

Examples:

* "What is the average sales by category?"
* "Show the top 10 products by revenue."
* "How many orders were placed in each region?"

The system:

1. Converts the user query into a Python-based analysis prompt.
2. Executes the code safely.
3. Returns the result to the user.

---

### 2. Data Visualization

The assistant can automatically generate charts based on user queries.

Examples:

* "Show a bar chart of sales by category."
* "Plot the distribution of ratings."
* "Visualize the top 5 products by revenue."

Charts are displayed in the **Visualization section** of the application.

---

### 3. Dataset Upload

Users upload their dataset in **CSV format (.csv)**.
Once uploaded, the dataset becomes available for analysis through natural language queries.

---

### 4. Prompt Data Visualization *(Work in Progress)*

This feature will show how user questions are transformed into prompts sent to the LLM.

Planned capabilities:

* Display the generated prompt
* Show intermediate reasoning steps
* Improve transparency of AI decision-making

---

## Tech Stack

**Frontend**

* Streamlit

**Backend**

* Python

**AI Framework**

* LangChain

**LLM Provider**

* Groq API (LLaMA models)

**Data Processing**

* Pandas

**Execution Environment**

* Python REPL Tool (LangChain)

---

## Project Structure

```
AI-Data-Analyst-Assistant
│
├── app.py
├── text_analysis.py
├── visualization.py
├── .env
└── README.md
```

---

## Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## Example Workflow

1. Upload a dataset **(.csv)**
2. Ask questions about the data
3. View analysis results
4. Generate visualizations
5. Explore insights instantly

---

## Example Queries

* "What is the average price of products?"
* "Show the top 10 products by rating."
* "Plot rating distribution."
* "Which category has the highest sales?"

---

## Future Improvements

* Prompt visualization and explainability
* Support for additional dataset formats
* Advanced statistical analysis
* Dashboard-style visual analytics
* Multi-dataset support

---

## Author

**Markandey Vatsa**
B.Tech Computer Science Engineering,
Interested in **AI application development, and Intelligent Systems and Java Backend Development (Developing scalable applications)**


## Visit the link to try: 
**https://ai-data-analyst-assistant-aacygtf4mcnnv3dpczi29h.streamlit.app/**

---


