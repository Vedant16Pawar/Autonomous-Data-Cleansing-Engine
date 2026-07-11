from backend.agent.agent import agent_executor

response = agent_executor.invoke(
    {
        "input": """
Input CSV Path:
sample.csv

Cleaning Instruction:
Remove duplicate rows.
Fill missing Age values with the median.
Fill missing City values with "Unknown".
"""
    }
)

print("\n========== FINAL RESPONSE ==========\n")
print(response)