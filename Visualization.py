import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

load_dotenv()

model = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)


def clean_code(code):
    """
    Removes markdown formatting that LLMs sometimes generate
    """
    code = code.replace("```python", "")
    code = code.replace("```", "")
    return code.strip()


def run_visualization(df, query):

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
- The dataframe is already available as df
- pandas is available as pd
- seaborn is available as sns
- matplotlib.pyplot is available as plt
- Always start with: fig, ax = plt.subplots(figsize=(12,6))
- Plot using ax
- Do NOT use plt.show()
- Use sns.set_theme(style="whitegrid") for styling if needed
- Use seaborn color palettes when appropriate
- Graph should be relevant to the user's question and the data provided
- Graph should be visually appealing and easy to understand
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
        exec(generated_code, {}, local_env)
    except Exception as e:
        raise RuntimeError(f"Visualization generation failed: {e}")

    fig = local_env.get("fig")

    if fig is None:
        fig = plt.gcf()

    return fig