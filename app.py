import streamlit as st
from openai import OpenAI
import os 

api_key = st.secrets["openai"]["OPENAI_API_KEY"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return None

def generate_investment_advice(income, expenses, current_investments, risk_tolerance, goals):
    savings = income - expenses

    strategy_prompt = f"""
    Given the following financial information:
    Monthly Income: ${income}
    Monthly Expenses: ${expenses}
    Monthly Savings: ${savings}
    Current Investments: {current_investments}
    Risk Tolerance (1-10): {risk_tolerance}
    Investment Goals: {goals}

    Please generate an investment strategy table in the following format:

    ## Strategy Overview 

    | Investment | Amount |
    |------------|--------|
    | [Investment 1] | $X.XX |
    | [Investment 2] | $X.XX |
    | [Investment 3] | $X.XX |
    | [Investment 4] | $X.XX |
    | [Investment 5] | $X.XX |
    | [Investment 6] | $X.XX |
    | [Investment 7] | $X.XX |
    | | **Total** | **$Y.YY** |

    Guidelines:
    1. Choose appropriate investments based on the user's risk tolerance, goals, and current investments.
    2. Include a mix of ETFs, individual stocks, and other investment vehicles as appropriate.
    3. Consider including categories like "Emergency Fund" or "High-Yield Savings" if appropriate.
    4. The number of investments can vary, but aim for 5-8 distinct categories.
    5. Allocate the funds across the investments based on the risk tolerance and goals provided.
    6. The total must exactly equal ${savings:.2f}, which is the difference between income and expenses. Display the actual calculated total, not the word "Total". ALL THE ROWS SHOULD ADD UP TO THE ACTUAL TOTAL.
    7. Do not include any text before or after the table. Only return the table itself.
    8. When suggesting stocks, list each stock ticker separately with its specific investment amount.
    9. For ETFs, you may group them or list individually based on importance.
    10. Ensure all amounts add up correctly and match the total savings amount.
    """

    investment_strategy = get_llm_response(strategy_prompt)

    if investment_strategy is None:
        print("Failed to get investment strategy from OpenAI")
        return "Error: Could not generate investment strategy."

    return investment_strategy

# The rest of your Streamlit code remains the same
st.set_page_config(page_title="Intelligent Investment Advisor", page_icon="💼", layout="wide")

st.title("Mint: Intelligent Investment Advisor")
st.subheader("buildspace n&w s5 | gaudamire.")

st.write("Please provide your financial information to receive personalized investment advice.")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Monthly Income ($)", min_value=0, step=100)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, step=100)
    current_investments = st.text_area("Current Investments (describe briefly)")

with col2:
    risk_tolerance = st.slider("Risk Tolerance", 1, 10, 5)
    goals = st.text_area("Investment Goals")

if st.button("Generate Advice"):
    if income > 0 and expenses > 0:
        with st.spinner("Generating your personalized investment strategy..."):
            investment_strategy = generate_investment_advice(income, expenses, current_investments, risk_tolerance, goals)

        if "Error" not in investment_strategy:
            st.markdown(investment_strategy)
            st.warning("Disclaimer: This advice is generated by an AI model and should not be considered as professional financial advice. Please consult with a qualified financial advisor before making any investment decisions.")
        else:
            st.error("An error occurred while generating advice. Please try again later.")
    else:
        st.error("Please enter valid income and expense amounts.")

st.sidebar.title("About")
st.sidebar.info("This is an AI-powered investment advisor. It provides personalized investment strategies based on your financial situation and goals.")
