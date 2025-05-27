# File: interaction_network_coloured.py

import matplotlib

matplotlib.use("Agg")
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.cm import get_cmap
from matplotlib.colors import to_hex
from pathlib import Path

# Nodes grouped by function (colors will reflect groups)
groups = {
    "Electrolytes": ["Sodium (Na)", "Potassium (K)", "Phosphorus (P)"],
    "Bone/Structure": [
        "Calcium (Ca)",
        "Magnesium (Mg)",
        "Fluoride (F)",
        "Silicon (Si)",
        "Boron (B)",
    ],
    "Blood & Oxygen": ["Iron (Fe)", "Cobalt (Co)", "Copper (Cu)"],
    "Enzyme Cofactors": [
        "Zinc (Zn)",
        "Manganese (Mn)",
        "Chromium (Cr)",
        "Molybdenum (Mo)",
        "Nickel (Ni)",
        "Vanadium (V)",
    ],
    "Thyroid & Hormones": ["Iodine (I)", "Selenium (Se)", "Lithium (Li)"],
}

all_nodes = [node for group in groups.values() for node in group]

# Relation edges
edges = [
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
    ("Boron (B)", "Calcium (Ca)", "boosts"),
    ("Boron (B)", "Magnesium (Mg)", "boosts"),
    ("Silicon (Si)", "Calcium (Ca)", "boosts"),
    ("Fluoride (F)", "Calcium (Ca)", "inhibits"),
    ("Vanadium (V)", "Iron (Fe)", "inhibits"),
    ("Nickel (Ni)", "Zinc (Zn)", "inhibits"),
    ("Cobalt (Co)", "Iron (Fe)", "inhibits"),
    ("Lithium (Li)", "Iodine (I)", "inhibits"),
]

# Assign colors to groups
color_map = get_cmap("tab10")
group_colors = {group: to_hex(color_map(i)) for i, group in enumerate(groups)}
node_colors = {}
for group, nodes in groups.items():
    for node in nodes:
        node_colors[node] = group_colors[group]

# Build graph
G = nx.DiGraph()
G.add_nodes_from(all_nodes)
for u, v, rel in edges:
    G.add_edge(u, v, relation=rel)

# Layout
pos = nx.spring_layout(G, k=0.8, seed=42)

# Plot
plt.figure(figsize=(14, 14))
node_color_list = [node_colors[n] for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=node_color_list, node_size=600)

# Node labels
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontsize=8.5, ha="center", va="center")

# Edges and symbols
for u, v, d in G.edges(data=True):
    style = "dashed" if d["relation"] == "inhibits" else "solid"
    label = "−" if d["relation"] == "inhibits" else "+"
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v)],
        style=style,
        connectionstyle="arc3,rad=0.15",
        arrowstyle="-|>",
        arrowsize=12,
        width=1.3,
    )
    xm, ym = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
    plt.text(xm, ym, label, fontsize=11, ha="center", va="center")

# Custom legends
from matplotlib.patches import Patch

group_legend = [Patch(color=hex, label=grp) for grp, hex in group_colors.items()]
line_legend = [
    Line2D([0], [0], linestyle="solid", lw=1.5, color="black", label="Boosts (+)"),
    Line2D([0], [0], linestyle="dashed", lw=1.5, color="black", label="Inhibits (−)"),
]

plt.legend(handles=group_legend + line_legend, loc="upper left", fontsize=9)
plt.title("Micronutrient Interaction Network (Grouped by Biological Role)", fontsize=14)
plt.axis("off")

# Save
Path(".github/resources").mkdir(parents=True, exist_ok=True)
plt.savefig(
    ".github/resources/micronutrient_network_coloured.png", dpi=300, bbox_inches="tight"
)
plt.close()
