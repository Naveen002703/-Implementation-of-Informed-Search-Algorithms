import streamlit as st
import heapq

st.set_page_config(page_title="Informed Search Algorithms", layout="wide")

st.title("🔍 Lab Program 2: Informed Search Algorithms")
st.subheader("Greedy Best-First Search and A* Algorithm")

# ---------------------------------------
# Sidebar Inputs
# ---------------------------------------
st.sidebar.header("Graph Input")

edges_input = st.sidebar.text_area(
    "Enter edges with cost (format: A B 1)",
    """A B 1
A C 4
B D 2
C D 1
D E 3"""
)

heuristic_input = st.sidebar.text_area(
    "Enter heuristic values (format: Node Value)",
    """A 7
B 6
C 2
D 1
E 0"""
)

start = st.sidebar.text_input("Start Node", "A")
goal = st.sidebar.text_input("Goal Node", "E")

# ---------------------------------------
# Graph Creation
# ---------------------------------------
def create_graph(edges_text):
    graph = {}
    for line in edges_text.strip().split("\n"):
        u, v, cost = line.split()
        cost = int(cost)
        
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
            
        graph[u].append((v, cost))
    
    return graph

def create_heuristic(h_text):
    h = {}
    for line in h_text.strip().split("\n"):
        node, value = line.split()
        h[node] = int(value)
    return h

graph = create_graph(edges_input)
heuristic = create_heuristic(heuristic_input)

st.subheader("📌 Graph Representation (Adjacency List)")
st.json(graph)

st.subheader("📌 Heuristic Function h(n)")
st.json(heuristic)

# ---------------------------------------
# Greedy Best-First Search
# ---------------------------------------
def greedy_best_first(graph, start, goal, h):
    visited = set()
    pq = [(h[start], start, 0, [start])]  # (priority, node, cost, path)

    while pq:
        _, node, cost, path = heapq.heappop(pq)

        if node == goal:
            return path, cost

        if node not in visited:
            visited.add(node)

            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (h[neighbor], neighbor, cost + edge_cost, path + [neighbor]))

    return None, None

# ---------------------------------------
# A* Algorithm
# ---------------------------------------
def a_star(graph, start, goal, h):
    pq = [(h[start], start, 0, [start])]  # (f(n), node, g(n), path)
    visited = {}

    while pq:
        f, node, g, path = heapq.heappop(pq)

        if node == goal:
            return path, g

        if node not in visited or g < visited[node]:
            visited[node] = g

            for neighbor, cost in graph[node]:
                g_new = g + cost
                f_new = g_new + h[neighbor]
                heapq.heappush(pq, (f_new, neighbor, g_new, path + [neighbor]))

    return None, None

# ---------------------------------------
# Execute
# ---------------------------------------
if st.button("Run Greedy & A*"):
    if start not in graph or goal not in graph:
        st.error("Invalid Start or Goal Node")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🟢 Greedy Best-First Search")
            path_g, cost_g = greedy_best_first(graph, start, goal, heuristic)
            if path_g:
                st.success("Path: " + " → ".join(path_g))
                st.info(f"Total Cost: {cost_g}")
            else:
                st.error("No Path Found")

        with col2:
            st.subheader("🔵 A* Search")
            path_a, cost_a = a_star(graph, start, goal, heuristic)
            if path_a:
                st.success("Path: " + " → ".join(path_a))
                st.info(f"Total Cost: {cost_a}")
            else:
                st.error("No Path Found")

# ---------------------------------------
# Comparison Section
# ---------------------------------------
st.subheader("📊 Optimality & Efficiency Comparison")

st.markdown("""
### 🟢 Greedy Best-First Search
- Uses: **f(n) = h(n)**
- Focuses only on heuristic
- Faster in many cases
- ❌ Not always optimal
- ❌ Can get stuck in local minima

### 🔵 A* Algorithm
- Uses: **f(n) = g(n) + h(n)**
- Considers both actual cost and heuristic
- ✅ Complete
- ✅ Optimal (if heuristic is admissible)
- Slightly higher memory usage

---

### 📌 Summary Table

| Algorithm | Evaluation Function | Optimal | Complete | Speed |
|------------|--------------------|----------|------------|--------|
| Greedy     | f(n) = h(n)        | ❌ No    | ❌ Not Always | Fast |
| A*         | f(n) = g(n)+h(n)   | ✅ Yes*  | ✅ Yes | Moderate |

\* A* is optimal if heuristic is admissible (never overestimates).
""")

st.info("A* generally gives better paths, while Greedy is faster but may produce suboptimal solutions.")
