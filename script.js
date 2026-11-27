
// Helper function to communicate with Flask
async function sendRequest(url, data = null) {
    const options = {
        method: data ? "POST" : "GET",
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || "Something went wrong");
    }

    return result;
}


// Display network and dashboard statistics
async function loadNetwork() {
    try {
        const graph = await sendRequest("/api/network");

        const users = Object.keys(graph);
        let connections = 0;

        const display = document.getElementById("networkDisplay");
        display.innerHTML = "";

        users.forEach(user => {
            connections += graph[user].length;

            const paragraph = document.createElement("p");
            paragraph.textContent =
                user + " → " + graph[user].join(", ");

            display.appendChild(paragraph);
        });

        if (users.length === 0) {
            display.textContent = "No users added yet.";
        }

        connections = connections / 2;

        const maxConnections = users.length * (users.length - 1) / 2;

        const density = maxConnections > 0
            ? (connections / maxConnections) * 100
            : 0;

        document.getElementById("totalUsers").textContent =
            users.length;

        document.getElementById("totalConnections").textContent =
            connections;

        document.getElementById("density").textContent =
            density.toFixed(1) + "%";

    } catch (error) {
        alert(error.message);
    }
}


// Add a new user
async function addUser() {
    const user = document.getElementById("newUser").value.trim();

    if (!user) {
        alert("Please enter a user name!");
        return;
    }

    try {
        const result = await sendRequest("/api/add-user", { user });

        alert(result.message);

        document.getElementById("newUser").value = "";

        loadNetwork();

    } catch (error) {
        alert(error.message);
    }
}


// Add friendship between two users
async function addConnection() {
    const user1 = document.getElementById("user1").value.trim();
    const user2 = document.getElementById("user2").value.trim();

    if (!user1 || !user2) {
        alert("Please enter both user names!");
        return;
    }

    try {
        const result = await sendRequest("/api/add-connection", {
            user1,
            user2
        });

        alert(result.message);

        document.getElementById("user1").value = "";
        document.getElementById("user2").value = "";

        loadNetwork();

    } catch (error) {
        alert(error.message);
    }
}


// Run BFS or DFS
async function runAlgorithm(type) {
    const user = document.getElementById("startUser").value.trim();

    if (!user) {
        alert("Please enter a starting user!");
        return;
    }

    try {
        const result = await sendRequest("/api/" + type, { user });

        document.getElementById("algorithmResult").textContent =
            type.toUpperCase() + " Traversal: " +
            result.result.join(" → ");

    } catch (error) {
        alert(error.message);
    }
}


// Find mutual friends
async function findMutual() {
    const user1 = document.getElementById("mutualUser1").value.trim();
    const user2 = document.getElementById("mutualUser2").value.trim();

    if (!user1 || !user2) {
        alert("Please enter both users!");
        return;
    }

    try {
        const result = await sendRequest("/api/mutual-friends", {
            user1,
            user2
        });

        document.getElementById("mutualResult").textContent =
            result.result.length > 0
                ? "Mutual Friends: " + result.result.join(", ")
                : "No mutual friends found.";

    } catch (error) {
        alert(error.message);
    }
}


// Find shortest path
async function findPath() {
    const start = document.getElementById("pathStart").value.trim();
    const end = document.getElementById("pathEnd").value.trim();

    if (!start || !end) {
        alert("Please enter both users!");
        return;
    }

    try {
        const result = await sendRequest("/api/shortest-path", {
            start,
            end
        });

        document.getElementById("pathResult").textContent =
            result.result
                ? "Shortest Path: " + result.result.join(" → ") +
                  " | Connections: " + (result.result.length - 1)
                : "No connection path found.";

    } catch (error) {
        alert(error.message);
    }
}


// Get friend recommendations
async function getRecommendations() {
    const user = document.getElementById("recommendUser").value.trim();

    if (!user) {
        alert("Please enter a user name!");
        return;
    }

    try {
        const result = await sendRequest("/api/recommendations", {
            user
        });

        const display = document.getElementById("recommendResult");

        if (result.result.length === 0) {
            display.textContent = "No recommendations available.";
            return;
        }

        display.textContent = result.result
            .map(item => item[0] + " - " + item[1] + " mutual friends")
            .join(" | ");

    } catch (error) {
        alert(error.message);
    }
}


// Load the network when the page opens
window.addEventListener("DOMContentLoaded", loadNetwork);
