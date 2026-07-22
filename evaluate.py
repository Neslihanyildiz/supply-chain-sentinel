from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from src.typosquat_analyzer import check_typosquat
from test_data.ground_truth import GROUND_TRUTH

y_true = []
y_pred = []

print("--- Evaluation Results ---\n")
for entry in GROUND_TRUTH:
    name = entry["name"]
    expected = entry["is_typosquat"]

    result = check_typosquat(name)
    predicted = result["is_suspicious"]

    y_true.append(expected)
    y_pred.append(predicted)

    status = "OK" if expected == predicted else "MISMATCH"
    print(f"[{status}] {name}: expected={expected}, predicted={predicted}")

precision = precision_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

print("\n--- Summary Metrics ---")
print(f"Precision: {precision:.2f}")
print(f"Recall:    {recall:.2f}")
print(f"F1 Score:  {f1:.2f}")
print(f"\nConfusion Matrix:")
print(f"  True Positives:  {tp}  (correctly flagged typosquats)")
print(f"  False Positives: {fp}  (legit packages wrongly flagged)")
print(f"  True Negatives:  {tn}  (correctly cleared legit packages)")
print(f"  False Negatives: {fn}  (missed typosquats)")