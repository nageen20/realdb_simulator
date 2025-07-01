from collections import defaultdict, deque

def get_table_generation_order(tables: dict) -> list:
    graph = defaultdict(list)
    indegree = defaultdict(int)

    # Build dependency graph
    for table_name, table_def in tables.items():
        for col_type in table_def["columns"].values():
            if "fk:" in col_type:
                ref_table = col_type.split("fk:")[1].split(".")[0]
                graph[ref_table].append(table_name)
                indegree[table_name] += 1
                if ref_table not in indegree:
                    indegree[ref_table] = 0

    # Kahn’s Algorithm for topological sort
    queue = deque([table for table in tables if indegree[table] == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(tables):
        raise ValueError("Cycle detected in table dependencies")

    return sorted_order
