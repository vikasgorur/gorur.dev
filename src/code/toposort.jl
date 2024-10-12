# %%
using Flux, ProgressMeter

# Input:

# Dependency graph for 4 nodes A, B, C, D
# is represented as a 4C2 = 6-dimensional vector

# Each dimension represents the relationship between two nodes
# A -> B, A -> C, A -> D, B -> C, B -> D, C -> D

# If A -> B, then the value is 1
# If B -> A, then the value is -1
# If there is no relationship, then the value is 0

# Output:
#
# The topological sort for the dependency graph.
# This is represented as a single number, indicating the permutation of the nodes

