from dataclasses import dataclass


@dataclass
class Node:
    label: str
    children: list["Node"]


def print_levels(root: Node):
    currentLevel = [root]
    nextLevel = []
    print(root.label)

    while len(currentLevel) > 0: 
        for node in currentLevel:
            nextLevel.extend(node.children)
            
        print(" ".join(n.label for n in nextLevel))
        currentLevel = nextLevel
        nextLevel = []


TREE = Node(label="1", children=[
    Node(label="2", children=[
        Node(label="4", children=[])
    ]),
    Node(label="3", children=[
        Node(label="5", children=[]),
        Node(label="6", children=[])
    ])
])

if __name__ == "__main__":
    print_levels(TREE)
