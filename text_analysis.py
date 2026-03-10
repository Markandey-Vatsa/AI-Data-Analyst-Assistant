import pandas as pd
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool

load_dotenv()

model = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-instruct"
)


def run_text_analysis(df, query):

    columns = df.columns.tolist()
    data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

    template = """
You are a data analysis assistant.

The dataframe is already loaded as df.

Available columns: {columns}
Their data types are: {data_types}

Generate ONLY valid Python code to answer the user's question.

Rules:
- Do NOT include markdown or ``` symbols
- Do NOT import libraries
- Use pandas operations
- ALWAYS use print() to display the final answer
- Do not explain anything
- Generate output in print function as if you are directly answering the user's question like a human, understant and answer the question directly in print function.
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

    generated_code = response.content.strip()

    if "print(" not in generated_code:
        generated_code = f"print({generated_code})"

    full_code = f"""
import pandas as pd
df = pd.DataFrame({df.to_dict()})
{generated_code}
"""

    python_repl = PythonREPLTool()

    result = python_repl.run(full_code)

    return result