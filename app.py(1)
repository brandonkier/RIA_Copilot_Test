from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HNW Financial Profile Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        .container { max-width: 600px; margin: auto; }
        label { display: block; margin-top: 20px; }
        input[type="file"] { margin-bottom: 10px; }
        input[type="submit"] { margin-top: 20px; padding: 10px 25px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload Household Financial Profile & Transaction History</h2>
        <form method="post" enctype="multipart/form-data">
            <label for="profile_file">Financial Profile (.csv or .xlsx):</label>
            <input type="file" name="profile_file" required>

            <label for="transaction_file">Transaction History (.csv or .xlsx):</label>
            <input type="file" name="transaction_file" required>

            <input type="submit" value="Analyze">
        </form>
    </div>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Analysis Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        .container { max-width: 900px; margin: auto; }
        pre { background: #f3f3f3; padding: 15px; border-radius: 6px; overflow-x: auto; }
        .back-btn { margin-top: 25px; display: inline-block; padding: 8px 18px; background: #d8d8d8; border-radius: 5px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Analysis Results</h2>
        <pre>{{ result }}</pre>
        <a class="back-btn" href="/">&#8592; Analyze Another Household</a>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        profile_file = request.files['profile_file']
        transaction_file = request.files['transaction_file']

        profile_data = profile_file.read().decode('utf-8', errors='ignore')
        transaction_data = transaction_file.read().decode('utf-8', errors='ignore')

        prompt = f"""
You are a Certified Financial Planner (CFP®) and a digital family office assistant trained in advanced financial analysis for high-net-worth (HNW) households.

I am uploading two files: (1) a complete household financial profile and (2) a categorized transaction history (3 years). These include:

- Net worth breakdown (assets & liabilities)
- Investment holdings across brokerage, retirement, and private equity accounts
- RSU vesting schedule
- 3 years of categorized transaction history from bank and credit card accounts
- Income summary
- Financial goals (e.g., retirement, education, real estate)
- [Etc.]

✅ Output Requirements:

Each of the following modules should be clearly labeled as a section in your response. All insights must tie directly to the data provided—quantify whenever possible and reference specific fields/values. Use professional, client-ready language with clear next steps, suitable for a white-glove, premium wealth management experience.

---

### 1. Financial Summary (Paraplanner-Style)
Provide a concise paragraph summarizing the household’s current financial standing, liquidity, and asset mix.

### 2. Net Worth & Liquidity
- Estimate total net worth, liquid net worth, and percent of assets that are illiquid (e.g., home equity, private equity).
- Identify any overconcentration in one account, asset class, or institution.

### 3. Cash Flow & Lifestyle Analysis
- Calculate average annual spending over the past 3 years.
- Highlight top spending categories (travel, dining, subscriptions, etc.).
- Assess discretionary vs. essential spending.
- Compare to benchmarks for similar HNW households.
- Assign a “Plan Health Score” (0–100) based on savings rate, lifestyle sustainability, and income stability.

### 4. Investment Review
- Evaluate portfolio diversification and asset allocation across all accounts.
- Flag concentrated positions (e.g., single-stock or sector risk).
- Review cost basis for unrealized gains/losses.
- Assess if the portfolio aligns with the client’s age and stated goals.

### 5. Tax Optimization
- Identify opportunities for tax-loss harvesting, Roth conversions (including backdoor), RSU liquidation timing, and tax-efficient rebalancing.
- Estimate potential tax savings.

### 6. Retirement Planning
- Assess retirement readiness based on target retirement age and income goal, current savings, and growth trajectory.
- Calculate required monthly savings/reallocation to stay on track, and summarize findings as in: “You need to save $X/month to retire at Y age with a $Z/year lifestyle.”

### 7. Education & Home Goal Planning
- Analyze the feasibility of college education funding and vacation/second home purchases.
- Recommend funding strategies (e.g., 529 plan, strategic asset sales, cash flow adjustments).

### 8. Estate & Risk Management
- Comment on the presence or absence of trusts, life/disability insurance, and beneficiary designations.
- Recommend review of estate structure, gifting strategies (e.g., DAF), and liability coverage as needed.

---

Guidelines:
- Each section must be clearly labeled.
- Quantify and cite the data for all insights (“You spent $48,000 last year on travel and restaurants”).
- Use professional, actionable language with clear next steps.
- Output in markdown or client-ready sections for easy formatting.

**Files provided:**

--- Household Profile ---
{profile_data}

--- Transaction History ---
{transaction_data}

Once the files are uploaded, confirm the data and begin the analysis.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096
        )

        result = response['choices'][0]['message']['content']
        return render_template_string(RESULT_HTML, result=result)

    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(debug=True)
