# Dataset schema (JSONL)

Each line is a JSON object with fields:
- image: path to image (relative)
- question: a natural language question about the image
- answer: ground-truth short answer (one sentence)

Example:
{"image":"data/images/library_001.jpg","question":"What place is this?","answer":"This is the college library where students are reading books."}
