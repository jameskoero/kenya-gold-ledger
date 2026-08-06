"""
02_network_analysis.py
-----------------------
Builds a graph connecting officials, athletes, and incidents from
controversies.json, to show how concentrated Kenyan sport-governance failure
actually is among a small, recurring set of names, rather than being spread
across many isolated actors.

This is not a standard Olympic-dataset feature. Every public Kenya-Olympics
resource I've found (Olympedia, Wikipedia, the Kaggle/GitHub dashboards) stops
at medals-by-country. Nobody has taken the governance record and treated it as
a graph. That's the point of this script: it's a genuinely new way to look at
the same public facts.

Method: bipartite-style graph, incidents as one node type, people (officials
and, where relevant, athletes) as the other, edges from people_implicated /
linked_medalists in controversies.json. A person who recurs across multiple
incidents gets a visibly higher degree, which is the whole finding.

Run:  python notebooks/02_network_analysis.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data"
VIZ = Path(__file__).resolve().parent.parent / "viz"
VIZ.mkdir(exist_ok=True)

CONTROVERSIES = json.loads((DATA / "controversies.json").read_text())["records"]

G = nx.Graph()

for rec in CONTROVERSIES:
    incident_id = rec["id"]
    incident_label = rec["title"]
    G.add_node(incident_id, kind="incident", label=incident_label,
               category=rec["category"])
    people = rec.get("people_implicated", []) + rec.get("linked_medalists", [])
    for person in people:
        # normalise trailing parenthetical role/context off the raw string
        clean = person.split(" (")[0].strip()
        if not clean:
            continue
        G.add_node(clean, kind="person")
        G.add_edge(clean, incident_id)

if G.number_of_nodes() == 0:
    print("No incidents with named people found — nothing to plot.")
else:
    people_nodes = [n for n, d in G.nodes(data=True) if d.get("kind") == "person"]
    incident_nodes = [n for n, d in G.nodes(data=True) if d.get("kind") == "incident"]

    degree = dict(G.degree())
    print("=== Degree centrality (recurrence across incidents) ===")
    for p in sorted(people_nodes, key=lambda n: -degree[n]):
        print(f"  {p}: appears in {degree[p]} incident(s)")

    pos = nx.spring_layout(G, seed=7, k=0.9)
    fig, ax = plt.subplots(figsize=(11, 8))

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#999999", width=1.2, alpha=0.6)

    person_sizes = [400 + 500 * (degree[n] - 1) for n in people_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=people_nodes, node_color="#BB0000",
                            node_size=person_sizes, ax=ax, alpha=0.9,
                            edgecolors="black", linewidths=0.8)
    nx.draw_networkx_nodes(G, pos, nodelist=incident_nodes, node_color="#D4AF37",
                            node_size=900, node_shape="s", ax=ax, alpha=0.9,
                            edgecolors="black", linewidths=0.8)

    labels = {n: n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)

    ax.set_title("Kenyan sport governance: who recurs across incidents\n"
                  "(circles = people, squares = incidents; larger circle = more incidents)",
                  fontsize=12, weight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(VIZ / "fig5_governance_network.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nFigure written to {VIZ / 'fig5_governance_network.png'}")
    print(f"Nodes: {G.number_of_nodes()} ({len(people_nodes)} people, "
          f"{len(incident_nodes)} incidents). Edges: {G.number_of_edges()}.")
