#!/usr/bin/env python
# encoding: utf-8
import json
import random

data = json.load(open("./faq.json", encoding="utf-8"))
random.shuffle(data)
data = data[:1000]
for index, each in enumerate(data):
    data[index]['index'] = index
qs = [each['q'] for each in data]
json.dump(data, open("faq.json", "wt", encoding="utf-8"), ensure_ascii=False, indent=4)
with open("faq.md", "wt", encoding="utf-8") as f:
    f.write("## intent:faq\n")
    for q in qs:
        f.write(f"- {q}\n")
