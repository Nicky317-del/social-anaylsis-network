
from collections import deque


def bfs(graph, start):

    visited = set()

    queue = deque()

    visited.add(start)
    queue.append(start)

    print("\nBFS Traversal:")

    while queue:

        user = queue.popleft()

        print(user, end=" ")

        for friend in graph[user]:

            if friend not in visited:

                visited.add(friend)
                queue.append(friend)


def dfs(graph, start, visited=None):

    if visited is None:
        visited = set()

    visited.add(start)

    print(start, end=" ")

    for friend in graph[start]:

        if friend not in visited:

            dfs(graph, friend, visited)


from collections import deque


def shortest_path(graph, start, end):

    if start not in graph or end not in graph:
        return None

    queue = deque([[start]])

    visited = set()
    visited.add(start)

    while queue:

        path = queue.popleft()

        user = path[-1]

        if user == end:
            return path

        for friend in graph[user]:

            if friend not in visited:

                visited.add(friend)

                new_path = path + [friend]

                queue.append(new_path)

    return None


