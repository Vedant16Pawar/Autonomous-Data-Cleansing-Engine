from backend.sandbox import run_code_in_docker

"""code = 
import pandas as pd

df = pd.read_csv("/sandbox/input.csv")

df = df.dropna(subset=["age"])

df.to_csv("/sandbox/output/output.csv", index=False)

"""

code = """
while True:
    pass
"""

result = run_code_in_docker(
    code=code,
    input_csv_path="sample.csv"
)

print(result)