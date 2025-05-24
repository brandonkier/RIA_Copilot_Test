import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.set_page_config(page_title="RIA Copilot", layout="wide")

# Set up API key input (securely)
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API Key", type="password")
client = OpenAI(api_key=api_key)

st.title("RIA Copilot")
st.markdown("---")

# Upload files
data_file = st.file_uploader("Upload Household Financial Dataset (.xlsx)", type=["xlsx"])
tx_file = st.file_uploader("Upload Transaction History (.xlsx)", type=["xlsx"])

def summarize_excel(file, label):
    """Outputs every row/column in every sheet as CSV, labeled by sheet."""
    sheet_summaries = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        sheet_summaries.append(
            f"#### {label} – {sheet}\n\n{df.to_csv(index=False)}"
        )
    return "\n\n".join(sheet_summaries)

if data_file and tx_file:
    try:
        profile_content = summarize_excel(data_file, "Financial Profile")
        tx_content = summarize_excel(tx_file, "Transaction History")
        combined_text = (
            "### Household Financial Profile\n\n"
            + profile_content
            + "\n\n### Transaction History\n\n"
            + tx_content
        )

        prompt = f"""
You are a Certified Financial Planner (CFP®) and a digital family office assistant trained in advanced financial analysis for high-net-worth (HNW) households.

You have been provided with a complete household financial profile and three years of categorized transaction history. The datasets are included below.

Each of the following modules should be clearly labeled as a section in your response. All insights must tie directly to the data provided—quantify whenever possible and reference specific fields/values. Use professional, client-ready language with clear next steps, suitable for a white-glove, premium wealth management experience.

**Analyze the uploaded data and provide the following:**

1. Financial Summary
Provide a concise paragraph summarizing the household’s current financial standing, liquidity, and asset mix.

2. Net Worth & Liquidity
Estimate total net worth, liquid net worth, and percent of assets that are illiquid (e.g., home equity, private equity).
Identify any overconcentration in one account, asset class, or institution.

3. Cash Flow & Lifestyle Analysis
Calculate average annual spending over the past 3 years.
Highlight top spending categories (travel, dining, subscriptions, etc.).
Assess discretionary vs. essential spending.
Compare to benchmarks for similar HNW households.
Assign a “Plan Health Score” (0–100) based on savings rate, lifestyle sustainability, and income stability.

4. Investment Review
Evaluate portfolio diversification and asset allocation across all accounts.
Flag concentrated positions (e.g., single-stock or sector risk).
Review cost basis for unrealized gains/losses.
Assess if the portfolio aligns with the client’s age and stated goals.

5. Tax Optimization
Identify opportunities for tax-loss harvesting, Roth conversions (including backdoor), RSU liquidation timing, and tax-efficient rebalancing.
Estimate potential tax savings.

6. Retirement Planning
Assess retirement readiness based on target retirement age and income goal, current savings, and growth trajectory.
Calculate required monthly savings/reallocation to stay on track, and summarize findings as in: “You need to save $X/month to retire at Y age with a $Z/year lifestyle.”

7. Education & Home Goal Planning
Analyze the feasibility of college education funding and vacation/second home purchases.
Recommend funding strategies (e.g., 529 plan, strategic asset sales, cash flow adjustments).

8. Estate & Risk Management
Comment on the presence or absence of trusts, life/disability insurance, and beneficiary designations.
Recommend review of estate structure, gifting strategies (e.g., DAF), and liability coverage as needed.

**Guidelines:**  
- Each section must be clearly labeled.  
- Quantify and cite the data for all insights (“You spent $48,000 last year on travel and restaurants”).  
- Use only standard markdown for all headings and tables (do NOT use code blocks).
- Render all tables in markdown table format, not inside triple-backticks.

---

### Household Financial Profile and Transaction History:
{combined_text}

Please begin your analysis immediately.
"""

        with st.spinner("Analyzing with GPT-4.1..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a CFP and digital wealth advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=4096  # Increase if you expect long responses and have API quota!
            )

        plan = response.choices[0].message.content
        st.markdown("## Financial Plan Output", unsafe_allow_html=True)
        st.markdown(plan, unsafe_allow_html=True)
        st.download_button("Download Plan as Text", plan, file_name="financial_plan.txt")

    except Exception as e:
        st.error(f"There was a problem parsing or analyzing the files: {e}")

elif not data_file or not tx_file:
    st.info("Upload both the household financial dataset **and** transaction history (.xlsx) files to get started.")
