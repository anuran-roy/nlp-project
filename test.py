# Enter Anuran and Braham and Ayush and Ramiz and move left and down and get cell and value
import json

a = input("\n\nEnter a string to generate the tree of:\n\n")

tree = [[y.strip() for y in x.strip().split()] for x in a.split("and ")]
tree2 = []

for i in range(len(tree)):
    if len(tree[i]) == 1:
        tree2[-1] += list(tree[i])
    else:
        tree2.append(tree[i])

    # print(tree2)

for i in tree2:
    for j in range(len(i)):
        if j == 0:
            i[j] = i[j].lower()

print(f"\n\nCrudely Parsed Tree: {tree2}")

tree3 = []

keyword = None
arg = None
tpl = None

for i in tree2:
    if i[0] == "enter":
        keyword = i[0]
        arg = " and ".join(i[1:])
        tpl = tuple((keyword, arg))

    else:  # if i[0] == 'move':
        keyword = i[0]
        arg = i[1:]
        tpl = []
        for i in range(len(arg)):
            tpl += [tuple((keyword, arg[i]))]

    if type(tpl) == type(tuple()):
        tree3.append(tpl)
    elif type(tpl) == type([]):
        tree3 += tpl
    else:
        continue

print(tree3)
print(f"\n\nRefined Parsed Tree: {json.dumps(tree3, indent=4)}")
del tree
del tree2
