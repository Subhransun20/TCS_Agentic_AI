
import re
from pprint import pprint

# Compliance matrix configuration
compliance_matrix = {
    "Market Manipulation": {
        "keywords": ["insider", "manipulate", "pump", "tip"],
        "severity": 3,
        "action": "Escalate"
    },
    "Bribery": {
        "keywords": ["kickback", "cash deal", "gift", "quid pro quo"],
        "severity": 3,
        "action": "Escalate"
    },
    "Secrecy Violation": {
        "keywords": ["off-the-record", "confidential", "hide"],
        "severity": 2,
        "action": "Manual Review"
    },
    "Policy Breach": {
        "keywords": ["bypass", "unofficial", "shadow"],
        "severity": 2,
        "action": "Manual Review"
    },
    "Ethics Violation": {
        "keywords": ["harassment", "bully", "racist"],
        "severity": 3,
        "action": "Escalate"
    }
}

# Priority scoring logic
def determine_priority(score):
    if score >= 5:
        return "High 🔴"
    elif score >= 3:
        return "Medium 🟠"
    elif score >= 1:
        return "Low 🟢"
    else:
        return "None ✅"

# Compliance matrix analyzer
def analyze_email(email_text):
    total_score = 0
    matches = []

    for category, details in compliance_matrix.items():
        for keyword in details["keywords"]:
            if re.search(rf"\b{keyword}\b", email_text, re.IGNORECASE):
                matches.append({
                    "category": category,
                    "keyword": keyword,
                    "severity": details["severity"],
                    "action": details["action"]
                })
                total_score += details["severity"]
                break  # one match per category is sufficient

    result = {
        "priority": determine_priority(total_score),
        "score": total_score,
        "matches": matches
    }
    return result

# Placeholder for hybrid rule + LLM integration (can plug into OpenAI or LangChain)
def hybrid_reasoning(email_text):
    rule_result = analyze_email(email_text)

    # Optionally combine this with LLM-based classification for more nuance
    # E.g., use GPT to validate the findings and assign final label
    # For now, return rule-based result
    return rule_result

# Sample execution
if __name__ == "__main__":
    email = """
    Please keep this deal off-the-record. The supplier agreed to give us a small gift to push it through.
    """
    print("📩 Email Text:")
    print(email.strip())
    print("\n🧠 Compliance Matrix Analysis:")
    pprint(hybrid_reasoning(email))
