# src/eval_utils.py
import json

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def run_basic_eval(fn_infer, jsonl_path):
    data = load_jsonl(jsonl_path)
    correct = 0
    total = 0
    for entry in data:
        image_path = entry["image"]
        q = entry["question"]
        expected = entry.get("answer","").lower()
        try:
            from PIL import Image
            img = Image.open(image_path).convert("RGB")
            res = fn_infer(img, q)
            got = res.get("answer","").lower()
            total += 1
            if expected in got or got in expected:
                correct += 1
        except Exception as e:
            print("Error", e)
    print(f"Accuracy (basic substring match): {correct}/{total} = {correct/total if total else 0:.2f}")
