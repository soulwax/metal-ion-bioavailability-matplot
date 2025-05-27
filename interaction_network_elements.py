import math
import matplotlib.pyplot as plt
import networkx as nx

# Expanded nutrient list
nodes = [
    "Calcium (Ca)",
    "Magnesium (Mg)",
    "Iron (Fe)",
    "Zinc (Zn)",
    "Copper (Cu)",
    "Manganese (Mn)",
    "Selenium (Se)",
    "Iodine (I)",
    "Chromium (Cr)",
    "Molybdenum (Mo)",
    "Sodium (Na)",
    "Potassium (K)",
    "Phosphorus (P)",
    "Boron (B)",
    "Silicon (Si)",
    "Fluoride (F)",
    "Vanadium (V)",
    "Nickel (Ni)",
    "Cobalt (Co)",
    "Lithium (Li)",
]

# Edge list: (source, target, relation)
edges = [
    # Previous edges
    ("Calcium (Ca)", "Iron (Fe)", "inhibits"),
    ("Calcium (Ca)", "Magnesium (Mg)", "inhibits"),
    ("Magnesium (Mg)", "Calcium (Ca)", "boosts"),
    ("Zinc (Zn)", "Copper (Cu)", "inhibits"),
    ("Zinc (Zn)", "Iron (Fe)", "inhibits"),
    ("Iron (Fe)", "Zinc (Zn)", "inhibits"),
    ("Manganese (Mn)", "Iron (Fe)", "inhibits"),
    ("Molybdenum (Mo)", "Copper (Cu)", "inhibits"),
    ("Selenium (Se)", "Iodine (I)", "boosts"),
    ("Iron (Fe)", "Iodine (I)", "boosts"),
    ("Chromium (Cr)", "Iron (Fe)", "inhibits"),
    ("Phosphorus (P)", "Calcium (Ca)", "inhibits"),
    ("Sodium (Na)", "Potassium (K)", "inhibits"),
    ("Potassium (K)", "Sodium (Na)", "inhibits"),
    ("Sodium (Na)", "Calcium (Ca)", "inhibits"),
    ("Potassium (K)", "Calcium (Ca)", "boosts"),
    # New edges
    ("Boron (B)", "Calcium (Ca)", "boosts"),
    ("Boron (B)", "Magnesium (Mg)", "boosts"),
    ("Silicon (Si)", "Calcium (Ca)", "boosts"),
    ("Fluoride (F)", "Calcium (Ca)", "inhibits"),
    ("Vanadium (V)", "Iron (Fe)", "inhibits"),
    ("Nickel (Ni)", "Zinc (Zn)", "inhibits"),
    ("Cobalt (Co)", "Iron (Fe)", "inhibits"),
    ("Lithium (Li)", "Iodine (I)", "inhibits"),
]

# Build graph
G = nx.DiGraph()
for node in nodes:
    G.add_node(node)
for src, tgt, rel in edges:
    G.add_edge(src, tgt, relation=rel)

# Layout
pos = nx.spring_layout(G, k=0.8, seed=42)

# Draw
plt.figure(figsize=(12, 12))
nx.draw_networkx_nodes(G, pos, node_size=500)
# Draw labels
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontsize=8, ha="center", va="center")

# Draw edges with styles
for u, v, d in G.edges(data=True):
    style = "dashed" if d["relation"] == "inhibits" else "solid"
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v)],
        arrowstyle="-|>",
        arrowsize=12,
        connectionstyle="arc3,rad=0.1",
        style=style,
        width=1.2,
    )
    # Midpoint label
    xm, ym = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
    label = "−" if d["relation"] == "inhibits" else "+"
    plt.text(xm, ym, label, fontsize=10, ha="center", va="center")

# Legend
from matplotlib.lines import Line2D

legend_elems = [
    Line2D([0], [0], linestyle="solid", lw=1.2, label="Boosts (+)"),
    Line2D([0], [0], linestyle="dashed", lw=1.2, label="Inhibits (−)"),
]
plt.legend(handles=legend_elems, loc="upper left", fontsize=9)
plt.title("Comprehensive Micronutrient Interaction Network", fontsize=14)
plt.axis("off")
plt.show()
