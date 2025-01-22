# Steam Friend Crawler

Have you ever heard the saying, "There are only six degrees of separation between you and any person"? This project explores whether this concept holds true for Steam friends.

## About the Project

The Steam Friend Crawler starts by examining the friends list of one Steam user, then recursively traverses their friends, and so on. While technically capable of infinite expansion, the process becomes time-intensive as the network grows.

To better understand the connections between users, the project includes a tool to visualize the crawled data as a entity relationship graph. You can see an example [[here](https://idontcaramel.dev/steam_graph/entity_relationship.html)]. The provided example is intentionally limited in size since rendering a graph with 100,000 nodes can be resource-intensive.


