import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.set_page_config(page_title="HNW Financial Planning Copilot", layout="wide")

# Set up API key input (securely)
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API Key", type="password")
client = OpenAI(api_key=api_key)

st.title("Advisor Dashboard – HNW Client Copilot")
st.markdown("---")

# Upload files
data_file = st.file_uploader("Upload Household Financial Dataset (.xlsx)", type=["xlsx"])
tx_file = st.file_uploader("Upload Transaction History (.xlsx)", type=["xlsx"])

def summarize_excel(file, label):
    sheet_summaries = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        sheet_summaries.append(f"### {label}: {sheet}\n\n" + df.head(5).to_markdown(index=False))
    return "\n\n".join(sheet_summaries)

if data_file and tx_file:
    try:
        profile_summary = summarize_excel(data_file, "Financial Profile")
        tx_summary = summarize_excel(tx_file, "Transaction History")
        combined_text = f"{profile_summary}\n\n{tx_summary}"

        # Prepare the prompt
        prompt = f"""You are a Certified Financial Planner (CFP®) acting as a virtual advisor for high-net-worth households.

Below is a client's financial dataset, including a family financial profile and three years of transaction history.

Analyze this data and provide the following:

1. A short financial summary (paraplanner style)
2. A net worth and liquidity breakdown
3. Cash flow & lifestyle analysis
4. Investment review
5. Tax optimization insights
6. Retirement planning feasibility
7. Education and home goal planning
8. Estate & risk management observations

Be specific. Include quantified insights and actionable advice where possible.

Client Dataset Preview:
{combined_text}
"""

        with st.spinner("Analyzing with GPT-4..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a CFP and digital wealth advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=2500
            )

        plan = response.choices[0].message.content
        st.markdown("##Financial Plan Output")
        st.markdown(plan)
        st.download_button("Download Plan as Text", plan, file_name="financial_plan.txt")

    except Exception as e:
        st.error(f"There was a problem parsing the files: {e}")

elif not data_file or not tx_file:
    st.info("Upload both the household financial dataset **and** transaction history (.xlsx) files to get started.")
