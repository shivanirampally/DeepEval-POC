import numpy as np
import pandas as pd


scores = np.array([0.91, 0.82, 0.65, 0.74, 0.45])

print("Scores:", scores)
print("Average score:", np.mean(scores))
print("Highest score:", np.max(scores))
print("Lowest score:", np.min(scores))


evaluation_data = {
    "test_case": ["TC001", "TC002", "TC003", "TC004", "TC005"],
    "score": scores,
    "status": ["PASS", "PASS", "FAIL", "PASS", "FAIL"]
}

report = pd.DataFrame(evaluation_data)

print("\nEvaluation Report:")
print(report)