import marimo

__generated_with = "0.6.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import random
    import networkx as nx


    def random_dep_graph(N):
        G = nx.DiGraph()  # Initialize a directed graph

        # Track the nodes that have been added to the graph
        nodes = list(range(N))
        random.shuffle(nodes)  # Shuffle the nodes to randomize the order of addition

        for i in range(N):
            current_node = nodes[i]
            possible_parents = nodes[:i]  # Only nodes that have been added earlier

            if possible_parents:
                num_parents = random.randint(1, min(i, 6))  # Random number of dependencies
                parents = random.sample(possible_parents, num_parents)
                for parent in parents:
                    G.add_edge(parent, current_node)

            else:
                # If it's the first node, just add it without any dependencies
                G.add_node(current_node)

        return G
    return nx, random, random_dep_graph


@app.cell
def __(nx, random_dep_graph):
    import matplotlib.pyplot as plt

    N = 10  # Number of nodes in the graph
    G = random_dep_graph(N)

    # Draw the graph
    pos = nx.spring_layout(G)  # Positions for all nodes
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=12, font_weight="bold", arrows=True)
    plt.title("Random Dependency Graph")
    plt.show()
    return G, N, plt, pos


@app.cell
def __(G, nx):
    nx.to_dict_of_lists(G)
    return


@app.cell
def __():
    def naive_topo_sort(g):
        pass
    return naive_topo_sort,


if __name__ == "__main__":
    app.run()
