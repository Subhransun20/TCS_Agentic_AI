
import streamlit as st
import openai
import os
import re

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or replace with actual key

# Define violation severity keywords
severity_keywords = {
    "market manipulation": 3,
    "bribery": 3,
    "quid pro quo": 2,
    "off-the-record": 2,
    "confidential": 1,
    "insider": 3,
    "kickback": 3,
    "non-disclosure": 1
}

# Priority Matrix logic
def calculate_priority(classification, email_text):
    severity_score = 0
    for keyword, score in severity_keywords.items():
        if re.search(rf"\b{keyword}\b", email_text, re.IGNORECASE):
            severity_score += score

    # Classification score
    class_score = {"Compliant": 0, "Suspicious": 1, "Non-Compliant": 2}.get(classification, 0)

    # Final weighted priority
    total_score = class_score + severity_score

    if total_score >= 5:
        return "High 🔴"
    elif total_score >= 3:
        return "Medium 🟠"
    elif total_score >= 1:
        return "Low 🟢"
    else:
        return "None ✅"

# Build prompt
def build_prompt(email_text):
    return f"""
You are a compliance agent for a bank. Classify the following email as:
1. Compliant
2. Suspicious
3. Non-Compliant

Email:
"""
{email_text}
"""

Respond in JSON format:
{{
  "classification": "<Compliant|Suspicious|Non-Compliant>",
  "violation_reason": "<brief explanation>",
  "suggested_action": "<Manual Review|Escalate|Archive>"
}}
"""

# LLM classifier
def get_compliance_output(email_text):
    prompt = build_prompt(email_text)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI compliance monitoring assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

# Streamlit UI
st.set_page_config(page_title="AI Compliance Agent", layout="wide")
st.title("📩 AI-Powered Email Compliance Classifier")

email_input = st.text_area("Paste an email for compliance review:", height=200)

if st.button("🔍 Analyze Email"):
    if not email_input.strip():
        st.warning("Please paste some email content to analyze.")
    else:
        with st.spinner("Analyzing..."):
            llm_output = get_compliance_output(email_input)
            st.json(llm_output)

            # Extract classification
            match = re.search(r'"classification":\s*"(.+?)"', llm_output)
            classification = match.group(1) if match else "Unknown"

            # Calculate priority
            priority = calculate_priority(classification, email_input)

            st.markdown(f"### 🧠 Classification: `{classification}`")
            st.markdown(f"### 🔥 Priority Level: **{priority}**")
