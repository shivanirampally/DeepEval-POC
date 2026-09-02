scores = [0.91, 0.82, 0.65, 0.74, 0.45]
threshold = 0.70

def evaluate_score(score, threshold):
    return "PASS" if score >= threshold else "FAIL"

for score in scores:
    status = evaluate_score(score, threshold)
    print(f"Result for score {score}: {status}")