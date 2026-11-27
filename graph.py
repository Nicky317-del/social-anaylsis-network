
class SocialNetwork:

    def __init__(self):
        self.graph = {}

    # Add a new user
    def add_user(self, user):
        if user not in self.graph:
            self.graph[user] = []
            print(user, "added successfully!")
        else:
            print("User already exists!")

    # Add friendship between two users
    def add_connection(self, user1, user2):

        if user1 not in self.graph:
            self.add_user(user1)

        if user2 not in self.graph:
            self.add_user(user2)

        if user2 not in self.graph[user1]:
            self.graph[user1].append(user2)
            self.graph[user2].append(user1)
            print("Connection added successfully!")
        else:
            print("Connection already exists!")

    # Display all users and their connections
    def display_network(self):
        print("\n----- SOCIAL NETWORK -----")

        for user, friends in self.graph.items():
            print(user, "->", friends)
