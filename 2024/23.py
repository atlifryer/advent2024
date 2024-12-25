import sys
from collections import defaultdict
from itertools import combinations

lines = sys.stdin.read().strip().split("\n")
computers = set()

for line in lines:
    computer1 = line.split("-")[0]
    computer2 = line.split("-")[1]
    computers.add(computer1)
    computers.add(computer2)

connections = defaultdict(set)

for line in lines:
    computer1, computer2 = line.split("-")
    connections[computer1].add(computer2)
    connections[computer2].add(computer1)

triangles = set()
for computer in computers:
    for neighbor1 in connections[computer]:
        for neighbor2 in connections[computer]:
            if neighbor1 != neighbor2 and neighbor2 in connections[neighbor1]:
                triangle = tuple(sorted([computer, neighbor1, neighbor2]))
                triangles.add(triangle)

triangles_with_t = [
    triangle for triangle in triangles if any(c.startswith("t") for c in triangle)
]

# part 1
print(len(triangles_with_t))


# part 2
def bron_kerbosch(R, P, X, connections, cliques):
    if not P and not X:
        cliques.append(R)
        return
    pivot = next(iter(P)) if P else None
    for v in P - (connections[pivot] if pivot else set()):
        bron_kerbosch(
            R | {v}, P & connections[v], X & connections[v], connections, cliques
        )
        P.remove(v)
        X.add(v)


def find_largest_clique(computers, connections):
    cliques = []
    bron_kerbosch(set(), set(computers), set(), connections, cliques)
    max_clique = max(cliques, key=len)
    return max_clique


largest_clique = find_largest_clique(computers, connections)
password = ",".join(sorted(largest_clique))
print(password)
