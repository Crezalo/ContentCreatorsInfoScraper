import os
import re

with open("iteration_complete/joined_distinct.tsv", "r", encoding="utf-8") as f:
    text = f.read().split("\n")
text = [x.split("\t") for x in text]

for i,x in enumerate(text):
    try:
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text[i][3])
        text[i].append(",".join(emails))
    except Exception as e:
        print(i)

text = ["\t".join(x) for x in text]

with open("iteration_complete/joined_distinct_withEmails.tsv","w",encoding="utf-8") as f:
    for x in text:
        f.write(x + "\n")

