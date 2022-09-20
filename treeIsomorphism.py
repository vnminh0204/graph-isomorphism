from graph_io import *
from datetime import datetime
import math
# input is a graph G, output if G is a tree or not
# tree is connected graph with e = v - 1
def isTree(G: "Graph"):
    for v in G.vertices:
        v.explored = False
    root = G.vertices[0]
    root.explored = True
    countConnected = 0
    queue = []
    queue.append(root)
    while len(queue) > 0:
        node = queue.pop(0)
        countConnected += 1
        for nei in node.neighbours:
            if nei.explored:
                continue
            nei.explored = True
            queue.append(nei)
    return countConnected == len(G.vertices) and len(G.vertices) == len(G.edges) + 1

    

#input is a tree, output is the center or double center of this tree
def findCenter(tree: "Graph"):
    n = len(tree.vertices)
    leaves = []
    for i in tree.vertices:
        i.d = i.degree
        if i.d <= 1:
            leaves.append(i)
            i.d = 0
        # print(i, i.d)
    processedLeaves = len(leaves)

    while processedLeaves < n:
        # print(processedLeaves)
        newLeaves = []
        for u in leaves:
            for v in u.neighbours:
                v.d -= 1
                if (v.d == 1):
                    newLeaves.append(v)
            u.d = 0

        processedLeaves += len(newLeaves)
        leaves = newLeaves
    return leaves

# input is a node, build tree using node as root
def buildTree(node):
    for n in node.neighbours:
        if node.parent is not None and n == node.parent:
            continue
        n.parent = node
        node.children.append(n)
        buildTree(n)
    return node

# encode a tree corresspoding to the node as root
def encode(node):
    if (node == None):
        return "";
    labels = []
    for c in node.children:
        labels.append(encode(c))
    labels.sort()
    sb = ""
    for label in labels:
        sb += (label)
    return "(" + sb + ")"

# check if two tree is isomorphic, return the number of possible mapping
def checkTreeIsormophic(tree1: "Graph", tree2: "Graph"):
    if (len(tree1.vertices) < 1 or len(tree2.vertices) < 1):
        return False
    count = 0
    x1, x2 = findCenter(tree1), findCenter(tree2)
    center1 = buildTree(x1[0])
    tree1Encoding = encode(center1)
    for center in x2:
        buildTree(center)
        tree2Encoding = encode(center)
        if tree1Encoding == tree2Encoding:
            count += 1
    if count > 0:
        return True, count*possibleEncodeCount(tree1Encoding)
    return False, 0

# clean the tree
def clean(tree: "Graph"):
    for v in tree.vertices:
        v.children = []
        v.parent = None
        v.d = 0

# recursively calculate possible of tree return this encode
def possibleEncodeCount(code):
    # base case: encode like (())
    if len(code) <= 4:
        return 1
    # map of subtree
    sub = {}
    balance = 1
    start = 1
    i = 2
    while i < len(code) - 1:
        if code[i] == ")":
            balance -= 1
        else:
            balance += 1
        i += 1
        # when we meet a fine close of a bracket
        if balance == 0:
            # count the number of subtree with the same encoding (one step child tree)
            subTree = code[start:i]
            sub[subTree] = sub.get(subTree, 0) + 1
            # mark start to current cursor and continue finding
            start = i
    result = 1
    for tree in sub:
        # print(tree, sub[tree])
        result *= math.factorial(sub[tree])
        result *= (possibleEncodeCount(tree) ** sub[tree])
    return result


def countAutAlone(tree):
    clean(tree)
    centers = findCenter(tree)
    center = buildTree(centers[0])
    code = encode(center)
    return len(centers) * possibleEncodeCount(code)
# with open("products216.grl") as f:
#     L = load_graph(f, read_list=True)
#     # g = L[0][2]
#     # with open('mygraph.dot', 'w') as f:
#     #     write_dot(g, f)
#     for i in range(len(L[0])):
#         print(i, isTree(L[0][i]))
#         for j in range(i+1, len(L[0])):
#             clean(L[0][i])
#             clean(L[0][j])
#             if (isTree(L[0][i]) and isTree(L[0][j])):
#                 print(i, j, checkIsormophic(L[0][i], L[0][j]))

