# Read graph instance: V vertices, E edges, m colors
V = int(input().strip())
E = int(input().strip())
m = int(input().strip())

# No need for more than V colors: keeps output size reasonable
effective_m = min(m, max(V, 1))

edges = []
deg = [0] * (V + 1) # degree to detect isolated vertices

# Read edges
for _ in range(E):
    u, v = map(int, input().split())
    if u == v:
        continue
    edges.append((u, v))
    deg[u] += 1
    deg[v] += 1

# Count isolated vertices (must be added to some scene)
isolated_count = 0
for v in range(1, V + 1):
    if deg[v] == 0:
        isolated_count += 1

n = V + 3 # Roles: 1=p1, 2=p2, 3=bridge, 4..V+3=graph roles
k = effective_m + 2 # Actors: 1,2 are divas: 3..k are color actors
s = len(edges) + 2 + isolated_count # Scenes: edge scenes + 2 diva scenes + isolated scenes

out = []
out.append(str(n))
out.append(str(s))
out.append(str(k))

# Fixed roles for p1, p2, and bridge actor p3
out.append("1 1")
out.append("1 2")
out.append("1 3")

# Graph roles can only use color actors 3..k
allowed = []
for a in range(3, k + 1):
    allowed.append(str(a))
allowed_string = " ".join(allowed)

role_line = str(effective_m) + " " + allowed_string
for _ in range(V):
    out.append(role_line)

# Force both divas to participate, but never together
out.append("2 1 3")
out.append("2 2 3")

for v in range(1, V + 1): # Isolated vertex roles must appear in at least one scene
    if deg[v] == 0:
        out.append("2 1 " + str(v + 3))

for u, v in edges: # Each graph edge becomes one scene (adjacent vertices must differ)
    out.append("2 " + str(u + 3) + " " + str(v + 3))

print("\n".join(out))
