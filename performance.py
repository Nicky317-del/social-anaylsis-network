
import time
import random
from collections import deque


# Create a sample social network
def generate_network(size):

    graph = {}

    for i in range(size):
        graph[i] = []

    # Connect users in a chain
    for i in range(size - 1):
        graph[i].append(i + 1)
        graph[i + 1].append(i)

    # Add some random connections
    random.seed(42)

    for i in range(size):
        for j in range(3):
            friend = random.randint(0, size - 1)

            if friend != i and friend not in graph[i]:
                graph[i].append(friend)
                graph[friend].append(i)

    return graph


# BFS performance
def bfs_test(graph):

    visited = set()
    queue = deque([0])

    visited.add(0)

    while queue:

        user = queue.popleft()

        for friend in graph[user]:

            if friend not in visited:
                visited.add(friend)
                queue.append(friend)


# DFS performance
def dfs_test(graph):

    visited = set()
    stack = [0]

    while stack:

        user = stack.pop()

        if user not in visited:

            visited.add(user)

            for friend in graph[user]:
                if friend not in visited:
                    stack.append(friend)


# Compare algorithm performance
def performance_analysis():

    sizes = [100, 500, 1000, 5000]

    print("\n----- PERFORMANCE ANALYSIS -----")

    print("Users\tBFS Time\tDFS Time")

    for size in sizes:

        graph = generate_network(size)

        # Measure BFS
        start = time.perf_counter()
        bfs_test(graph)
        bfs_time = time.perf_counter() - start

        # Measure DFS
        start = time.perf_counter()
        dfs_test(graph)
        dfs_time = time.perf_counter() - start

        print(
            size, "\t",
            round(bfs_time, 6), "\t",
            round(dfs_time, 6)
        )
