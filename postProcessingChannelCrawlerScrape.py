import os

os.system("cat iteration_complete/*.tsv > iteration_complete/joined.tsv")

with open("iteration_complete/joined.tsv", "r") as f:
    text = f.read().split("\n")

print("Total Length : " + str(len(text)))
print("Distinct Length : " + str(len(list(set(text)))))

with open("iteration_complete/joined_distinct.tsv", "w") as f:
    for x in list(set(text)):
        f.write(x + "\n")
