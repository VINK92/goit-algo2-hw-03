from collections import deque, defaultdict

def edmonds_karp(capacity, source, sink):
    """
    Реалізація алгоритму Едмондса-Карпа для знаходження максимального потоку.

    Args:
        capacity: Словник з пропускними здатностями ребер (u, v): capacity[(u, v)]
        source: Вершина-джерело
        sink: Вершина-сток

    Returns:
        Максимальний потік і деталі про фактичні потоки між вершинами.
    """
    flow = defaultdict(int)
    total_flow = 0

    def bfs():
        parent = {source: None}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in parent and capacity[(u, v)] - flow[(u, v)] > 0:
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    while (path := bfs()) is not None:
        # Знаходимо мінімальну пропускну здатність уздовж шляху
        min_capacity = float('inf')
        v = sink
        while v != source:
            u = path[v]
            min_capacity = min(min_capacity, capacity[(u, v)] - flow[(u, v)])
            v = u

        # Оновлюємо потоки уздовж шляху
        v = sink
        while v != source:
            u = path[v]
            flow[(u, v)] += min_capacity
            flow[(v, u)] -= min_capacity
            v = u

        total_flow += min_capacity

    return total_flow, flow

# Побудова графа
edges = [
    ("T1", "S1", 25), ("T1", "S2", 20), ("T1", "S3", 15),
    ("T2", "S3", 15), ("T2", "S4", 30), ("T2", "S2", 10),
    ("S1", "M1", 15), ("S1", "M2", 10), ("S1", "M3", 20),
    ("S2", "M4", 15), ("S2", "M5", 10), ("S2", "M6", 25),
    ("S3", "M7", 20), ("S3", "M8", 15), ("S3", "M9", 10),
    ("S4", "M10", 20), ("S4", "M11", 10), ("S4", "M12", 15),
    ("S4", "M13", 5), ("S4", "M14", 10),
]

capacity = defaultdict(int)
adj = defaultdict(list)
for u, v, cap in edges:
    capacity[(u, v)] = cap
    adj[u].append(v)
    adj[v].append(u)

# Джерело та сток
source = "T1_T2"
sink = "M1_M14"

# Додамо об'єднане джерело та сток для зручності розрахунків
for terminal in ["T1", "T2"]:
    capacity[(source, terminal)] = float('inf')
    adj[source].append(terminal)
    adj[terminal].append(source)

for store in ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14"]:
    capacity[(store, sink)] = float('inf')
    adj[store].append(sink)
    adj[sink].append(store)

# Розрахунок максимального потоку
max_flow, flow = edmonds_karp(capacity, source, sink)

# Аналіз результатів
print(f"Максимальний потік: {max_flow}\n")

print("Фактичні потоки між вершинами:")
for (u, v), f in flow.items():
    if f > 0 and (u != source and v != sink):
        print(f"{u} -> {v}: {f}")

# Підготовка таблиці результатів
results = []
for terminal in ["T1", "T2"]:
    for store in ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14"]:
        if flow[(terminal, store)] > 0:
            results.append((terminal, store, flow[(terminal, store)]))

print("\nТаблиця результатів:")
print("Термінал\tМагазин\tФактичний Потік")
for terminal, store, f in results:
    print(f"{terminal}\t{store}\t{f}")
