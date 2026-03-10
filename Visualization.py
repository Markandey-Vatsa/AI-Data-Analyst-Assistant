import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

load_dotenv()

model = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)


def clean_code(code):
    """
    Removes markdown formatting that LLMs sometimes generate
    """
    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.replace("plt.show()", "")
    return code.strip()


def convert_datetime_columns(df):
    """
    Attempt automatic datetime conversion for object columns
    """
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    return df


def run_visualization(df, query):

    # convert possible date columns
    df = convert_datetime_columns(df)

    columns = df.columns.tolist()
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

    template = """
You are a Python visualization assistant.

The dataframe is already loaded as df.

Columns: {columns}
Data types: {data_types}

Generate ONLY valid Python code.

Rules:
- Do NOT write explanations
- Do NOT use markdown
- Do NOT import libraries
- Use only df that already exists
- Always start with: fig, ax = plt.subplots(figsize=(12,6))
- Plot using ax
- Use matplotlib or seaborn
- Prefer seaborn plots
- Do NOT use plt.show()
- Generate ONLY ONE visualization
- Do NOT create multiple figures
- Do NOT manually set ticks
- Do NOT use ax.set_xticks() or ax.set_xticklabels()
- Let matplotlib automatically handle axis ticks
- If datetime operations are needed convert using pd.to_datetime()
- If selecting multiple columns use df[['col1','col2']] not df['col1','col2']
"""

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "{query}")
        ]
    )

    prompt = prompt_template.format_messages(
        columns=columns,
        data_types=data_types,
        query=query
    )

    response = model.invoke(prompt)

    generated_code = clean_code(response.content)

    local_env = {
        "df": df,
        "plt": plt,
        "sns": sns,
        "pd": pd,
        "np": np
    }

    try:
        exec(generated_code, local_env)
    except Exception as e:
        raise RuntimeError(
            f"Visualization generation failed: {e}\n\nGenerated Code:\n{generated_code}"
        )

    fig = local_env.get("fig")

    if fig is None:
        fig = plt.gcf()

    return fig