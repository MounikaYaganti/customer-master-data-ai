import ollama


def analyze_duplicate(customer, potential_duplicates):
    prompt = f"""
You are an enterprise customer master data analyst.

Analyze the potential duplicate identified by a deterministic
duplicate detection system.

IMPORTANT RULES:
- Use only the information provided.
- Do not invent missing values.
- Do not recalculate the similarity score.
- Do not change the risk level provided by the Python system.
- The AI recommendation is advisory only.
- The final decision must be made by a human Master Data reviewer.

NEW CUSTOMER:
{customer}

POTENTIAL DUPLICATES:
{potential_duplicates}

You MUST provide ALL SIX sections below.

1. Potential Duplicate Risk:
Use the risk level provided in the potential duplicate record.

2. Evidence:
List only the important matching attributes.

3. Explanation:
Briefly explain why the record requires review.

4. Recommended Action:
State whether manual review is recommended.

5. AI Recommendation:
Choose exactly ONE:
Likely Duplicate – Manual Review Required
Possible Duplicate – Further Investigation Recommended
Low Duplicate Probability – Likely New Customer

6. AI Confidence Score:
Provide a number between 0 and 100 followed by %.

Do not skip sections 5 or 6.
Keep the response concise and business-friendly.
"""
    

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]