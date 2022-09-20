from collections import deque
from basicpermutationgroup import *
from permv2 import permutation
from treeIsomorphism import *

color = []
mapNum = []
generate_set = []


def disjoint_union(grapha: "Graph", graphb: "Graph") -> "Graph":
    result = Graph(grapha.directed, 0)
    for u in grapha.vertices:
        u._graph = result
        u.graph_label = "A"
        result.add_vertex(u)
    for e in grapha.edges:
        result.add_edge(e)
    for u in graphb.vertices:
        u._graph = result
        u.graph_label = "B"
        result.add_vertex(u)
    for e in graphb.edges:
        result.add_edge(e)

    newlabel = 0
    for u in result.vertices:
        u.label = newlabel
        newlabel += 1
    return result


def is_balanced(colors_dict):
    global color
    color_count_grapha = dict()
    color_count_graphb = dict()

    for c in colors_dict.keys():
        classc = colors_dict[c]
        for u in classc:
            if u.graph_label == "A":
                if color[u.label] not in color_count_grapha:
                    color_count_grapha[c] = 1
                else:
                    color_count_grapha[c] += 1
            elif u.graph_label == "B":
                if color[u.label] not in color_count_graphb:
                    color_count_graphb[c] = 1
                else:
                    color_count_graphb[c] += 1
    return color_count_grapha == color_count_graphb


def uniform_initialization(g: "Graph"):
    global color
    colors_dict = dict()
    colors_dict[0] = set()
    color = [0] * len(g.vertices)
    for u in g.vertices:
        colors_dict[0].add(u)
        color[u.label] = 0
    return colors_dict


def computesetA(classC):
    num_nb_to_c_of = dict()
    for u in classC:
        for v in u.neighbours:
            if v not in num_nb_to_c_of.keys():
                num_nb_to_c_of[v] = 1
            else:
                num_nb_to_c_of[v] += 1

    sets_by_num_neighbors_to_c = dict()
    for u in num_nb_to_c_of.keys():
        num_neighbors_to_c = num_nb_to_c_of[u]
        if num_neighbors_to_c not in sets_by_num_neighbors_to_c.keys():
            sets_by_num_neighbors_to_c[num_neighbors_to_c] = set()
            sets_by_num_neighbors_to_c[num_neighbors_to_c].add(u)
        else:
            sets_by_num_neighbors_to_c[num_neighbors_to_c].add(u)

    return sets_by_num_neighbors_to_c


def fast_color_refinement(g: "Graph", colors_dict):
    global color
    queue = deque()
    in_queue = [False] * (len(g.vertices) + 10)
    done = [False] * (len(g.vertices) + 10)

    for c in colors_dict.keys():
        classC = colors_dict[c]
        for u in classC:
            color[u.label] = c
        queue.append(c)
        in_queue[c] = True

    while len(queue) > 0:
        c = queue.pop()
        done[c] = True
        in_queue[c] = False

        # use color c to refine other color classes
        classC = colors_dict[c]
        # slide 75 lemma
        sets_by_num_neighbors_to_c = computesetA(classC)

        for num_neighbors in sets_by_num_neighbors_to_c.keys():
            ai = sets_by_num_neighbors_to_c[num_neighbors]
            # refine(colors_dict, ai)
            transition_from_Ci_to_classC = dict()

            # bullet 1 slide 73
            for trans in ai:
                u = trans
                color_of_trans = color[u.label]

                if color_of_trans not in transition_from_Ci_to_classC.keys():
                    transition_from_Ci_to_classC[color_of_trans] = [u]
                else:
                    transition_from_Ci_to_classC[color_of_trans].append(u)

            for color_of_trans in transition_from_Ci_to_classC.keys():
                if len(transition_from_Ci_to_classC[color_of_trans]) < len(colors_dict[color_of_trans]):
                    new_split_set_ci = set()
                    new_color = len(colors_dict)
                    for trans in transition_from_Ci_to_classC[color_of_trans]:
                        u = trans
                        colors_dict[color_of_trans].remove(u)
                        new_split_set_ci.add(u)
                        color[u.label] = new_color
                    colors_dict[new_color] = new_split_set_ci

                    if in_queue[color_of_trans]:
                        queue.append(new_color)
                        in_queue[new_color] = True
                    else:
                        if len(colors_dict[new_color]) < len(colors_dict[color_of_trans]):
                            queue.append(new_color)
                            in_queue[new_color] = True
                        else:
                            queue.append(color_of_trans)
                            in_queue[color_of_trans] = True
                else:
                    if (not done[color_of_trans]) and (not in_queue[color_of_trans]):
                        queue.append(color_of_trans)
                        in_queue[color_of_trans] = True

    return colors_dict


def update_neighbor_color(u):
    global color
    nb_color_dict = dict()
    for nb in u.neighbours:
        if color[nb.label] not in nb_color_dict:
            nb_color_dict[color[nb.label]] = 1
        else:
            nb_color_dict[color[nb.label]] += 1
    u.neighbor_colors = nb_color_dict


def neighbor_color_check(u, v):
    return u.neighbor_colors == v.neighbor_colors


def color_refinement(g: "Graph", colors_dict):
    global color
    max_color = -1
    for c in colors_dict.keys():
        classc = colors_dict[c]
        for u in classc:
            color[u.label] = c
        if c > max_color:
            max_color = c

    for u in g.vertices:
        update_neighbor_color(u)

    i = 0

    while True:
        break_check = True
        i = i + 1

        used_color = [False] * (max_color+1)
        examined = [False] * len(g.vertices)
        new_colors_dict = dict()
        for c in colors_dict.keys():
            same_color_vertices = colors_dict[c]

            for u in same_color_vertices:
                if examined[u.label] == False:
                    examined[u.label] = True
                    cellu = set()
                    cellu.add(u)
                    for v in same_color_vertices:
                        if (u != v) and (examined[v.label] == False):
                            if neighbor_color_check(u,v) == True:
                                examined[v.label] = True
                                cellu.add(v)
                    if not used_color[c]:
                        used_color[c] = True
                        new_colors_dict[c] = cellu
                    else:
                        break_check = False
                        max_color += 1
                        for x in cellu:
                            color[x.label] = max_color
                        new_colors_dict[max_color] = cellu
        colors_dict = new_colors_dict.copy()

        for u in g.vertices:
            update_neighbor_color(u)

        if break_check:
            return colors_dict


def check_isomorphism(g: "Graph", old_colors_dict):
    colors_dict = fast_color_refinement(g, old_colors_dict)

    if not is_balanced(colors_dict):
        return 0

    if is_define_a_bijection_with_twins(colors_dict):
        return 1

    choosen_color = -1
    maxVal = 0
    for c in colors_dict.keys():
        classCsize = len(colors_dict[c]) - count_twins_class_c(colors_dict[c])
        if (classCsize >= 4) and (classCsize > maxVal):
            choosen_color = c
            maxVal = classCsize
            # break
    classc = colors_dict[choosen_color]
    listb = set()

    num = 0

    x = None
    for u in classc:
        if u.numtwins >= 0:
            if u.graph_label == "A":
                x = u
            elif u.graph_label == "B":
                listb.add(u)

    for y in listb:
        # BRANCHING RULE
        if (x.twinType == y.twinType) and (x.numtwins == y.numtwins):

            new_colors_dict = hard_copy(colors_dict,x,y, choosen_color)

            # count isomorphism with new color for x and y
            num = check_isomorphism(g, new_colors_dict)
            if num == 1:
                return 1
    return num


# make copy of color dict with new color for x,y
def hard_copy(color_dicts,x, y, chosen_color):
    new_dict = dict()

    for c in color_dicts.keys():
        if c != chosen_color:
            classC = color_dicts[c]
            new_dict[c] = set()
            for u in classC:
                new_dict[c].add(u)
    new_dict[chosen_color] = set()
    new_color = len(color_dicts)
    new_dict[new_color] = set()
    for u in color_dicts[chosen_color]:
        if u.numtwins < 0:
            if (u.twinmaster.label == x.label) or (u.twinmaster.label == y.label):
                new_dict[new_color].add(u)
            else:
                new_dict[chosen_color].add(u)
        elif u.numtwins >= 0:
            if (u.label != x.label) and (u.label != y.label):
                new_dict[chosen_color].add(u)
    new_dict[new_color].add(x)
    new_dict[new_color].add(y)
    return new_dict


def twins_detection(g: "Graph"):
    twins_dict = dict()
    # detect false twins
    for u in g.vertices:
        u.numtwins = 0
        u.twinType = 0
        nb_list = frozenset(set(u.neighbours))
        if nb_list not in twins_dict:
            twins_dict[nb_list] = [u]
        else:
            twins_dict[nb_list].append(u)

    for nb_list in twins_dict.keys():
        if len(twins_dict[nb_list]) >= 2:
            verticies_list = twins_dict[nb_list]
            verticies_list[0].numtwins = len(twins_dict[nb_list])
            verticies_list[0].twinType = 1
            for i in range(1,len(verticies_list)):
                verticies_list[i].numtwins = -1
                verticies_list[i].twinmaster = verticies_list[0]
                verticies_list[i].twinType = 1
    # detect true twin
    twins_dict = dict()
    for u in g.vertices:
        if u.numtwins == 0:
            nb_list = set(u.neighbours)
            nb_list.add(u)
            nb_list = frozenset(nb_list)
            if nb_list not in twins_dict:
                twins_dict[nb_list] = [u]
            else:
                twins_dict[nb_list].append(u)

    for nb_list in twins_dict.keys():
        if len(twins_dict[nb_list]) >= 2:
            verticies_list = twins_dict[nb_list]
            verticies_list[0].numtwins = len(twins_dict[nb_list])
            verticies_list[0].twinType = 2
            for i in range(1, len(verticies_list)):
                verticies_list[i].numtwins = -1
                verticies_list[i].twinmaster = verticies_list[0]
                verticies_list[i].twinType = 2
    # for u in g.vertices:
    #     if u.numtwins < 0:
    #         g.del_vertex(u)
    # newlabel = 0
    # for u in g.vertices:
    #     u.label = newlabel
    #     newlabel += 1


def fact(x):
    ans = 1
    for num in range(2, x + 1):
        ans = ans * num
    return ans


def create_mapping(colors_dict):
    global mapNum
    mapping = [0] * len(colors_dict)
    # x is element of graph A
    # y is element of graph B
    x = None
    y = None

    for c in colors_dict.keys():
        colorClass = colors_dict[c]
        for u in colorClass:
            if u.numtwins >= 0:
                if u.graph_label == "A":
                    x = mapNum[u.label]
                elif u.graph_label == "B":
                    y = mapNum[u.label]
        mapping[x] = y

    return mapping


def count_twins_class_c(classc):
    cnt2 = 0
    for u in classc:
        if u.numtwins > 0:
            cnt2 += (u.numtwins-1)
    return cnt2


def is_define_a_bijection_with_twins(colors_dict):
    for c in colors_dict.keys():
        if (len(colors_dict[c])-count_twins_class_c(colors_dict[c])) != 2:
            return False
    return True


def generate_isomorphism(g: "Graph", old_colors_dict, foundTrivial):
    global mapNum
    global generate_set
    colors_dict = fast_color_refinement(g, old_colors_dict)

    if not is_balanced(colors_dict):
        return False

    if is_define_a_bijection_with_twins(colors_dict):
        if not foundTrivial:
            # initialize mapping number
            for c in colors_dict.keys():
                colorClass = colors_dict[c]
                for u in colorClass:
                    mapNum[u.label] = c
        else:
            mapping = create_mapping(colors_dict)
            permu_from_map = permutation(len(colors_dict), None, mapping)

            generate_set.append(permu_from_map)

        return True

    choosen_color = -1
    # BRANCHING RULE find biggest classC to skip the most number of branches
    maxVal = 0
    for c in colors_dict.keys():

        classCsize = len(colors_dict[c]) - count_twins_class_c(colors_dict[c])
        if (classCsize >= 4) and (classCsize > maxVal):
            maxVal = classCsize
            choosen_color = c

    classc = colors_dict[choosen_color]
    listb = set()

    x = None
    for u in classc:
        if u.numtwins >= 0:
            if u.graph_label == "A":
                x = u
            elif u.graph_label == "B":
                listb.add(u)

    foundIso = False
    for y in listb:
        # BRANCHING RULE
        if (x.twinType == y.twinType) and (x.numtwins == y.numtwins):
            new_colors_dict = hard_copy(colors_dict, x, y, choosen_color)

            # count isomorphism with new color for x and y
            # found trivial isomorphism or x=x
            if mapNum[y.label] == mapNum[x.label]:
                foundIso = generate_isomorphism(g, new_colors_dict, foundTrivial)
            else:
                # found isomorphism on right branch x != y
                foundIso = generate_isomorphism(g, new_colors_dict, foundTrivial = True) or foundIso
            if foundTrivial and foundIso:
                break
    return foundIso


def is_isomorphism(g1: "Graph", g2: "Graph"):
    if len(g1.vertices) != len(g2.vertices):
        return False

    if len(g1.edges) != len(g2.edges):
        return False
    g = disjoint_union(g1, g2)
    colors_dict = uniform_initialization(g)
    count = check_isomorphism(g, colors_dict)
    if count == 1:
        return True
    return False


def self_autoisomorphism_count(g: "Graph", copyg:"Graph"):
    count = 0
    self_disjoin = disjoint_union(g, copyg)
    global generate_set
    generate_set = []
    global mapNum
    mapNum = [-1] * len(self_disjoin.vertices)
    initial_color_dict = uniform_initialization(self_disjoin)
    found = generate_isomorphism(self_disjoin, initial_color_dict, False)

    if found:
        count = Order(generate_set)

    for u in self_disjoin.vertices:
        if (u.graph_label == "A") and (u.numtwins > 0):
            count = count * fact(u.numtwins)
    return count


if __name__ == '__main__':
    directory = 'bonus/3130bonus05GI.grl'
    with open(directory) as f:
        L = load_graph(f, read_list=True)
    with open(directory) as f:
        L2 = load_graph(f, read_list=True)

    val = "x"
    tree = False
    while True:
        val = input("Do you want to use tree processing? (Type y/n)")
        if (val == "y") or (val == "n"):
            break
    if val == "y":
        tree = True
    # tree = True
    gi = False
    aut = False
    val = "x"
    while True:
        val = input("Is it GI problem? (Type y/n)")
        if (val == "y") or (val == "n"):
            break
    if val == "y":
        gi = True
    val = "x"
    while True:
        val = input("Is it #Aut problem? (Type y/n)")
        if (val == "y") or (val == "n"):
            break
    if val == "y":
        aut = True

    start_time = datetime.now()

    if gi and not aut:
        examined_graph_index = [False]*len(L[0])
        treesList = []
        nonTreeList = []
        print("Sets of possibly isomorphic graphs:")
        for i in range(len(L[0])):
            if tree:
                if isTree(L[0][i]):
                    treesList.append((L[0][i], i))
                else:
                    nonTreeList.append((L[0][i], i))
            else:
                nonTreeList.append((L[0][i], i))
        start_time = datetime.now()
        for i in treesList:
            if not examined_graph_index[i[1]]:
                examined_graph_index[i[1]] = True
                isomorphism_set = [i[1]]
                final_count = -1
                for j in treesList:
                    if not examined_graph_index[j[1]]:
                        clean(i[0])
                        clean(j[0])
                        isIsomorphism, count = checkTreeIsormophic(i[0], j[0])
                        if isIsomorphism:
                            examined_graph_index[j[1]] = True
                            final_count = count
                            isomorphism_set.append(j[1])
                print(str(isomorphism_set) + " " + str(final_count))
        for i in nonTreeList:
            twins_detection(i[0])
        for i in range(len(nonTreeList)):
            if not examined_graph_index[nonTreeList[i][1]]:
                examined_graph_index[nonTreeList[i][1]] = True
                isomorphism_set = [nonTreeList[i][1]]
                for j in range(i+1, len(nonTreeList), 1):
                    if not examined_graph_index[nonTreeList[j][1]]:
                        if is_isomorphism(nonTreeList[i][0], nonTreeList[j][0]):
                            isomorphism_set.append(nonTreeList[j][1])
                            examined_graph_index[nonTreeList[j][1]] = True
                print(str(isomorphism_set))
    elif not gi and aut:
        treesList = []
        nonTreeList = []
        print("Graph: Number of automorphisms:")
        for i in range(len(L[0])):
            if tree:
                if isTree(L[0][i]):
                    treesList.append((L[0][i], i))
                else:
                    nonTreeList.append((L[0][i], i))
            else:
                nonTreeList.append((L[0][i], i))
        start_time = datetime.now()
        for i in treesList:
                isomorphism_set = [i[1]]
                final_count = countAutAlone(i[0])
                print(str(isomorphism_set) + ":   " + str(final_count))

        for i in nonTreeList:
            twins_detection(i[0])
        for i in range(len(nonTreeList)):
            twins_detection(L2[0][nonTreeList[i][1]])
            final_count = self_autoisomorphism_count(nonTreeList[i][0], L2[0][nonTreeList[i][1]])
            isomorphism_set = [nonTreeList[i][1]]
            print(str(isomorphism_set) + ":   " + str(final_count))

    elif gi and aut:
        examined_graph_index = [False]*len(L[0])
        treesList = []
        nonTreeList = []
        print("Sets of possibly isomorphic graphs:")
        for i in range(len(L[0])):
            if tree:
                if isTree(L[0][i]):
                    treesList.append((L[0][i], i))
                else:
                    nonTreeList.append((L[0][i], i))
            else:
                nonTreeList.append((L[0][i], i))
        start_time = datetime.now()
        for i in treesList:
            if not examined_graph_index[i[1]]:
                examined_graph_index[i[1]] = True
                isomorphism_set = [i[1]]
                final_count = -1
                for j in treesList:
                    if not examined_graph_index[j[1]]:
                        clean(i[0])
                        clean(j[0])
                        isIsomorphism, count = checkTreeIsormophic(i[0], j[0])
                        # print(i[1], j[1], checkIsormophic(i[0], j[0]))
                        if isIsomorphism:
                            examined_graph_index[j[1]] = True
                            final_count = count
                            isomorphism_set.append(j[1])
                print(str(isomorphism_set) + " " + str(final_count))

        for i in nonTreeList:
            twins_detection(i[0])
        for i in range(len(nonTreeList)):
            if not examined_graph_index[nonTreeList[i][1]]:
                twins_detection(L2[0][nonTreeList[i][1]])
                final_count = self_autoisomorphism_count(nonTreeList[i][0], L2[0][nonTreeList[i][1]])

                examined_graph_index[nonTreeList[i][1]] = True
                isomorphism_set = [nonTreeList[i][1]]
                for j in range(i+1, len(nonTreeList), 1):
                    if not examined_graph_index[nonTreeList[j][1]]:
                        if is_isomorphism(nonTreeList[i][0], nonTreeList[j][0]):
                            isomorphism_set.append(nonTreeList[j][1])
                            examined_graph_index[nonTreeList[j][1]] = True

                print(str(isomorphism_set) + " " + str(final_count))

    endtime = datetime.now()
    print(endtime - start_time)

    # check_fast_rfm = True
    # if check_fast_rfm:
    #     with open('SampleGraphsBasicColorRefinement/threepaths10240.gr') as f:
    #         time0 = datetime.now()
    #         L = load_graph(f)
    #         time1 = datetime.now()
    #         print("Load graph time: " + str(time1 - time0))
    #         colors_dict = fast_color_refinement(L, uniform_initialization(L))
    #         time2 = datetime.now()
    #         print("Processing time: " + str(time2 - time1))
    #
    # check_normal_rfm = False
    # if check_normal_rfm:
    #     with open('SampleGraphsBasicColorRefinement/threepaths10240.gr') as f:
    #         time0 = datetime.now()
    #         L = load_graph(f)
    #         time1 = datetime.now()
    #         print("Load graph time: " + str(time1 - time0))
    #         colors_dict = color_refinement(L, uniform_initialization(L))
    #         time2 = datetime.now()
    #         print("Processing time: " + str(time2 - time1))





