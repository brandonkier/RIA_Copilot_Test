
import streamlit as st
import pandas as pd
import openai
import os

# Set Streamlit page configuration FIRST
st.set_page_config(page_title="HNW Financial Planning Copilot", layout="wide")

# Set up API key input (can be hidden in deployment)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API Key", type="password")

st.title("💼 Advisor Dashboard – HNW Client Copilot")
st.markdown("---")

# Upload Excel file
data_file = st.file_uploader("Upload Household Financial Dataset (.xlsx)", type=["xlsx"])

# Placeholder for analysis output
if data_file:
    # Parse data for display and send to GPT
    try:
        xls = pd.ExcelFile(data_file)
        sheet_summaries = []

        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            sheet_summaries.append(f"### {sheet}\n\n" + df.head(5).to_markdown(index=False))

        combined_text = "\n\n".join(sheet_summaries)

        # Prepare the prompt (can use enhanced version from earlier)
        prompt = f"""
You are a Certified Financial Planner (CFP®) acting as a virtual advisor for high-net-worth households.

Below is a client's financial dataset, including bank transactions, investment holdings, RSUs, income, goals, and more.

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
            response = openai.ChatCompletion.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": "You are a CFP and digital wealth advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=2500
            )

        plan = response.choices[0].message.content
        st.markdown("## 🧠 Financial Plan Output")
        st.markdown(plan)

        # Optional: download/export
        st.download_button("Download Plan as Text", plan, file_name="financial_plan.txt")

    except Exception as e:
        st.error(f"There was a problem parsing the file: {e}")
else:
    st.info("Upload a .xlsx file to get started.")
