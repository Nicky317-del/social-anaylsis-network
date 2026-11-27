
# from graph import SocialNetwork
# from algorithms import bfs, dfs, shortest_path
# from recommendations import mutual_friends, recommend_friends
# from performance import performance_analysis


# # Create social network object
# network = SocialNetwork()


# # Main menu function
# def main_menu():

#     while True:

#         print("\n====================================")
#         print("       SOCIAL NETWORK ANALYSIS")
#         print("====================================")

#         print("1. Add User")
#         print("2. Add Connection")
#         print("3. Display Network")
#         print("4. BFS Traversal")
#         print("5. DFS Traversal")
#         print("6. Find Mutual Friends")
#         print("7. Shortest Connection Path")
#         print("8. Friend Recommendations")
#         print("9. Performance Analysis")
#         print("10. Exit")

#         choice = input("\nEnter your choice: ")

#         if choice == "1":

#             user = input("Enter user name: ")
#             network.add_user(user)

#         elif choice == "2":

#             user1 = input("Enter first user: ")
#             user2 = input("Enter second user: ")

#             network.add_connection(user1, user2)

#         elif choice == "3":

#             network.display_network()

#         elif choice == "4":

#             user = input("Enter starting user: ")

#             if user in network.graph:
#                 bfs(network.graph, user)
#             else:
#                 print("User not found!")

#         elif choice == "5":

#             user = input("Enter starting user: ")

#             if user in network.graph:
#                 dfs(network.graph, user)
#                 print()
#             else:
#                 print("User not found!")

#         elif choice == "6":

#             user1 = input("Enter first user: ")
#             user2 = input("Enter second user: ")

#             result = mutual_friends(
#                 network.graph, user1, user2
#             )

#             print("Mutual Friends:", result)

#         elif choice == "7":

#             start = input("Enter starting user: ")
#             end = input("Enter destination user: ")

#             path = shortest_path(
#                 network.graph, start, end
#             )

#             if path:
#                 print("Shortest Path:", " -> ".join(path))
#                 print("Number of connections:", len(path) - 1)
#             else:
#                 print("No connection path found!")

#         elif choice == "8":

#             user = input("Enter user name: ")

#             suggestions = recommend_friends(
#                 network.graph, user
#             )

#             if suggestions:
#                 print("\nFriend Recommendations:")

#                 for person, count in suggestions:
#                     print(person, "-", count, "mutual friends")
#             elif user in network.graph:
#                 print("No recommendations available!")

#         elif choice == "9":

#             performance_analysis()

#         elif choice == "10":

#             print("Thank you for using Social Network Analysis!")
#             break

#         else:

#             print("Invalid choice! Please try again.")


# # Start the application
# main_menu()


from graph import SocialNetwork
from algorithms import bfs, dfs, shortest_path
from recommendations import mutual_friends, recommend_friends
from performance import performance_analysis


# Create social network
network = SocialNetwork()


def line():
    print("=" * 55)


def heading(title):
    print("\n")
    line()
    print("             " + title)
    line()


def get_user_input(message):
    name = input(message).strip()

    if not name:
        print("Error: Name cannot be empty!")
        return None

    return name


def show_dashboard():
    total_users = len(network.graph)
    total_connections = sum(
        len(friends) for friends in network.graph.values()
    ) // 2

    heading("SOCIAL NETWORK DASHBOARD")

    print(f"  Total Users       : {total_users}")
    print(f"  Total Connections : {total_connections}")

    if total_users > 1:
        possible = total_users * (total_users - 1) / 2
        density = (total_connections / possible) * 100
        print(f"  Network Density   : {density:.2f}%")
    else:
        print("  Network Density   : 0.00%")

    line()


def display_menu():
    print("""
        1.  Add New User
        2.  Add Connection
        3.  Display Complete Network
        4.  Search User
        5.  BFS Traversal
        6.  DFS Traversal
        7.  Find Mutual Friends
        8.  Find Shortest Path
        9.  Friend Recommendations
        10. Performance Analysis
        11. Exit
    """)


def add_new_user():
    heading("ADD NEW USER")

    name = get_user_input("Enter user name: ")

    if name is None:
        return

    if name in network.graph:
        print("This user already exists!")
    else:
        network.add_user(name)
        print("User added successfully!")


def add_new_connection():
    heading("ADD CONNECTION")

    user1 = get_user_input("Enter first user: ")
    if user1 is None:
        return

    user2 = get_user_input("Enter second user: ")
    if user2 is None:
        return

    if user1 not in network.graph:
        print(f"User '{user1}' does not exist. Add the user first.")
        return

    if user2 not in network.graph:
        print(f"User '{user2}' does not exist. Add the user first.")
        return

    if user1 == user2:
        print("A user cannot connect to themselves!")
        return

    if user2 in network.graph[user1]:
        print("These users are already connected!")
        return

    network.add_connection(user1, user2)
    print("Connection created successfully!")


def display_network():
    heading("COMPLETE SOCIAL NETWORK")

    if not network.graph:
        print("No users found. Add users first.")
        return

    for user, friends in network.graph.items():
        print(f"\n{user}")
        if friends:
            print("  Friends:", ", ".join(friends))
        else:
            print("  Friends: No connections")

    line()


def search_user():
    heading("SEARCH USER")

    user = get_user_input("Enter user name to search: ")

    if user is None:
        return

    if user not in network.graph:
        print("User not found!")
        return

    friends = network.graph[user]

    print("\nUser found:", user)
    print("Total friends:", len(friends))
    print("Friends:", ", ".join(friends) if friends else "No friends yet")


def run_traversal(algorithm):
    heading(algorithm.upper() + " TRAVERSAL")

    start = get_user_input("Enter starting user: ")

    if start is None:
        return

    if start not in network.graph:
        print("Starting user does not exist!")
        return

    if algorithm == "bfs":
        result = bfs(network.graph, start)
    else:
        result = dfs(network.graph, start)

    print("\nTraversal order:")
    print(" -> ".join(result))


def find_mutual():
    heading("MUTUAL FRIENDS")

    user1 = get_user_input("Enter first user: ")
    if user1 is None:
        return

    user2 = get_user_input("Enter second user: ")
    if user2 is None:
        return

    if user1 not in network.graph or user2 not in network.graph:
        print("One or both users do not exist!")
        return

    result = mutual_friends(network.graph, user1, user2)

    if result:
        print("\nMutual friends:", ", ".join(result))
        print("Total mutual friends:", len(result))
    else:
        print("No mutual friends found.")


def find_shortest_path():
    heading("SHORTEST CONNECTION PATH")

    start = get_user_input("Enter starting user: ")
    if start is None:
        return

    end = get_user_input("Enter destination user: ")
    if end is None:
        return

    if start not in network.graph or end not in network.graph:
        print("One or both users do not exist!")
        return

    result = shortest_path(network.graph, start, end)

    if result:
        print("\nShortest path:")
        print(" -> ".join(result))
        print("Number of connections:", len(result) - 1)
    else:
        print("No connection path exists between these users.")


def show_recommendations():
    heading("FRIEND RECOMMENDATIONS")

    user = get_user_input("Enter user name: ")

    if user is None:
        return

    if user not in network.graph:
        print("User does not exist!")
        return

    recommendations = recommend_friends(network.graph, user)

    if not recommendations:
        print("No friend recommendations available.")
        return

    print("\nSuggested friends:")

    for index, item in enumerate(recommendations, start=1):
        friend, mutual_count = item
        print(
            f"{index}. {friend} "
            f"({mutual_count} mutual friends)"
        )


def run_performance():
    heading("PERFORMANCE ANALYSIS")

    print("Running BFS and DFS performance tests...")
    print("Please wait...\n")

    results = performance_analysis()

    if not results:
        print("Performance analysis completed.")
        return

    if isinstance(results, list):
        print("\nPerformance Results")
        line()

        for result in results:
            print(f"Users: {result['users']}")
            print(f"BFS Time: {result['bfs']} seconds")
            print(f"DFS Time: {result['dfs']} seconds")
            line()


def main():
    while True:
        show_dashboard()
        display_menu()

        choice = input("Enter your choice (1-11): ").strip()

        try:
            if choice == "1":
                add_new_user()

            elif choice == "2":
                add_new_connection()

            elif choice == "3":
                display_network()

            elif choice == "4":
                search_user()

            elif choice == "5":
                run_traversal("bfs")

            elif choice == "6":
                run_traversal("dfs")

            elif choice == "7":
                find_mutual()

            elif choice == "8":
                find_shortest_path()

            elif choice == "9":
                show_recommendations()

            elif choice == "10":
                run_performance()

            elif choice == "11":
                heading("EXIT")
                print("Thank you for using Social Network Analysis!")
                break

            else:
                print("Invalid choice! Please enter a number from 1 to 11.")

        except Exception as error:
            print("\nSomething went wrong:", error)
            print("Please check your input and try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
