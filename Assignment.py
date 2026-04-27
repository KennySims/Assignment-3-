from collections import deque

def BWParse(file):
    with open(file, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    vertex_tokens = raw_lines[0].split()
    n = len(vertex_tokens)

    vertex_ids = vertex_tokens
    num_to_token = {}
    for token in vertex_tokens:
        i = 0
        while i < len(token) and token[i].isdigit():
            i += 1
        num_to_token[token[:i]] = token

    adjacency_dict = {vertex_id: [] for vertex_id in vertex_ids}

    matrix_lines = raw_lines[1 : 1 + n]
    for row_index, line in enumerate(matrix_lines):
        values = line.split()
        for col_index, value in enumerate(values):
            if value == "1":
                adjacency_dict[vertex_ids[row_index]].append(vertex_ids[col_index])

    start_finish = raw_lines[1 + n].split()
    start, finish = start_finish[0], start_finish[1]
    start = num_to_token.get(start, start)
    finish = num_to_token.get(finish, finish)

    k = int(raw_lines[2 + n].split()[0])
    #print(adjacency_dict, k, start, finish)
    return adjacency_dict, k, start, finish

def runBW(adjacency_dict, k, start, finish):

    print(adjacency_dict, k, start, finish)
    queue = deque([(start, 0, [])])
    visited = set([start])

    while queue:
        current_vertex, depth, pathlist = queue.popleft()

        if current_vertex == finish and depth <= k:
            return True, pathlist + [current_vertex]

        if depth < k:
            for neighbor in adjacency_dict[current_vertex]:
                if neighbor not in visited:
                    if len(pathlist) < 2:
                        print("test")
                        if current_vertex[-1] == neighbor[-1]:
                            continue
                    elif current_vertex[-1] == neighbor[-1] or pathlist[-1][-1] == neighbor[-1]:
                        print("Skipping neighbor", neighbor, "from", current_vertex, "due to color constraint")
                        continue
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1, pathlist + [current_vertex]))

    return False, []

def parseDAGSP(file):
    with open(file, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    vertex_tokens = raw_lines[0].split()
    n = len(vertex_tokens)

    vertex_ids = vertex_tokens

    adjacency_dict = {vertex_id: [] for vertex_id in vertex_ids}

    matrix_lines = raw_lines[1 : 1 + n]
    for row_index, line in enumerate(matrix_lines):
        values = line.split()
        for col_index, value in enumerate(values):
            if value == "1":
                adjacency_dict[vertex_ids[row_index]].append(vertex_ids[col_index])

    start_finish = raw_lines[1 + n].split()
    start, finish = start_finish[0], start_finish[1]

    k = int(raw_lines[2 + n].split()[0])
    #print(adjacency_dict, k, start, finish)
    return adjacency_dict, k, start, finish
        
def transformDAGSP(adjacency_dict, k, start, finish):
    transformedadjacency_dict = {}
    newnodes = len(adjacency_dict.keys()) + 1
    for vertex, neighbors in adjacency_dict.items():
        transformedadjacency_dict.setdefault(str(vertex) + "w", [])
        for neighbor in neighbors:
            b_node = str(newnodes) + "b"
            r_node = str(newnodes + 1) + "r"
            neighbor_w = str(neighbor) + "w"
            if neighbor == start:
                    transformedadjacency_dict.setdefault(str(vertex) + "w", []).append(b_node)
                    transformedadjacency_dict.setdefault(b_node, []).append(neighbor_w)
                    transformedadjacency_dict.setdefault(b_node, []).append(str(vertex) + "w")
                    transformedadjacency_dict.setdefault(neighbor_w, []).append(b_node)
                    newnodes += 1
            else:
                transformedadjacency_dict.setdefault(str(vertex) + "w", []).append(b_node)
                transformedadjacency_dict.setdefault(b_node, []).append(r_node)
                transformedadjacency_dict.setdefault(b_node, []).append(str(vertex) + "w")
                transformedadjacency_dict.setdefault(r_node, []).append(b_node)
                transformedadjacency_dict.setdefault(r_node, []).append(neighbor_w)
                transformedadjacency_dict.setdefault(neighbor_w, []).append(r_node)
                newnodes += 2
    return transformedadjacency_dict, k*3, start+"w", finish+"w"
            
def main():

    adjacency_dict, k, start, finish = parseDAGSP("input2.txt")
    adjacency_dict, k, start, finish = transformDAGSP(adjacency_dict, k, start, finish)
    result, path = runBW(adjacency_dict, k, start, finish)
    print("YES" if result else "NO")
    if result:
        print("Path:", " -> ".join(path))

if __name__ == "__main__":
    main()
