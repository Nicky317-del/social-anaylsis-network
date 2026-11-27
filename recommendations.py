
def mutual_friends(graph, user1, user2):

    if user1 not in graph or user2 not in graph:
        print("User not found!")
        return []

    friends1 = set(graph[user1])
    friends2 = set(graph[user2])

    common_friends = friends1.intersection(friends2)

    return list(common_friends)


def recommend_friends(graph, user):

    if user not in graph:
        print("User not found!")
        return []

    recommendations = {}

    for friend in graph[user]:

        for potential_friend in graph[friend]:

            if (potential_friend != user and
                potential_friend not in graph[user]):

                if potential_friend not in recommendations:
                    recommendations[potential_friend] = 0

                recommendations[potential_friend] += 1

    sorted_recommendations = sorted(
        recommendations.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_recommendations

