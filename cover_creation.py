# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:03:01 2025

@author: Trabajador
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:35:02 2025

@author: Trabajador
"""

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import check_planarity
from math import dist
from random import randint

def createMosaicGraph(width_mm: float, height_mm: float, spacing_mm: float) -> nx.Graph:
    """
    Create a graph grid subdivided with diagonal connections.

    Parameters
    ----------
    width_mm : float
        Total width of the drawing area in millimeters.
    height_mm : float
        Total height of the drawing area in millimeters.
    spacing_mm : float
        Spacing between major grid lines in millimeters.

    Returns
    -------
    G : networkx.Graph
        The generated graph, with nodes positioned in a quarter-grid pattern
        and edges connecting them both within each cell and between adjacent cells.
    """
    G = nx.Graph()
    
    # Compute how many spacing intervals fit (plus one to include both ends)
    num_cols = int(width_mm // spacing_mm) + 1
    num_rows = int(height_mm // spacing_mm) + 1
    # Precompute quarter-spacing; every cell will be subdivided into a 4×4 quarter grid
    q = spacing_mm / 4.0

    # Define local node offsets (in quarters of the spacing) within each cell
    # These are (dx, dy) pairs relative to the cell's origin (j*spacing, i*spacing)
    local_offsets = [
        (1, 0), (0, 1),            # A1
        (1, 0), (2, 1),            # A2
        (0, 1), (1, 2),            # A3
        (2, 1), (1, 2),            # A4
        (3, 0), (2, 1),            # A5
        (3, 0), (4, 1),            # A6
        (2, 1), (3, 2),            # A7
        (4, 1), (3, 2),            # A8
        (1, 2), (0, 3),            # A9
        (1, 2), (2, 3),            # A10
        (0, 3), (1, 4),            # A11
        (2, 3), (1, 4),            # A12
        (3, 2), (2, 3),            # A13
        (3, 2), (4, 3),            # A14
        (2, 3), (3, 4),            # A15
        (4, 3), (3, 4),            # A16
    ]

    # Define edges within a single cell by pairing up entries in local_offsets
    # Each two consecutive offsets form one edge
    internal_edges = [
        (local_offsets[k][0]*q, local_offsets[k][1]*q,
         local_offsets[k+1][0]*q, local_offsets[k+1][1]*q)
        for k in range(0, len(local_offsets), 2)
    ]

    # Build nodes and internal edges for each cell
    for i in range(num_rows):
        for j in range(num_cols):
            # Only on even-indexed cells (matching original pattern)
            if (i % 2 == 0) and (j % 2 == 0):
                cell_origin = (j * spacing_mm, i * spacing_mm)
                # Add the subdivided nodes
                for dx, dy in [(ox*q, oy*q) for ox, oy in local_offsets]:
                    G.add_node((cell_origin[0] + dx, cell_origin[1] + dy))
                # Add the internal cell edges
                for x1, y1, x2, y2 in internal_edges:
                    G.add_edge(
                        (cell_origin[0] + x1, cell_origin[1] + y1),
                        (cell_origin[0] + x2, cell_origin[1] + y2),
                        distance = dist((cell_origin[0] + x1, cell_origin[1] + y1),
                                             (cell_origin[0] + x2, cell_origin[1] + y2)),
                        weight = randint(1, 10)
                    )

    # Now add the inter-cell “bridge” edges (A17–A20) between neighboring cells
    # Horizontal bridges: connect right-edge quarter-nodes of each cell to the next cell
    for i in range(0, num_rows, 2):
        for j in range(0, num_cols-2, 2):
            base_x = j * spacing_mm
            base_y = i * spacing_mm
            # vertical positions at 1/4 and 3/4 of the spacing
            y_positions = [base_y + spacing_mm/4, base_y + 3*spacing_mm/4]
            for y in y_positions:
                G.add_edge((base_x + spacing_mm, y),
                           (base_x + 2*spacing_mm, y),
                           distance = dist((base_x + spacing_mm, y),
                                                (base_x + 2*spacing_mm, y)),
                           weight = randint(20, 30))
                
    # Vertical bridges: connect bottom-edge quarter-nodes down to the cell below
    for i in range(0, num_rows-2, 2):
        for j in range(0, num_cols, 2):
            base_x = j * spacing_mm
            base_y = i * spacing_mm
            # horizontal positions at 1/4 and 3/4 of the spacing
            x_positions = [base_x + spacing_mm/4, base_x + 3*spacing_mm/4]
            for x in x_positions:
                G.add_edge((x, base_y + spacing_mm),
                           (x, base_y + 2*spacing_mm),
                           distance = dist((x, base_y + spacing_mm),
                                                 (x, base_y + 2*spacing_mm)),
                            weight = randint(20, 30))

    return G


def polygonArea(face, pos):
    """
    Calculate the area of a polygon using the shoelace formula.
    Args:
        face: List of vertex indices.
        pos: Dictionary mapping vertices to (x, y) coordinates.
    Returns:
        Area of the polygon.
    """

    # compute the 2D shoelace area of a face
    xs = [pos[n][0] for n in face]
    ys = [pos[n][1] for n in face]
    a = 0.0
    for i in range(len(face)):
        j = (i+1) % len(face)
        a += xs[i]*ys[j] - xs[j]*ys[i]
    return abs(a) * 0.5


def plotMosaic(width_mm, height_mm, spacing_mm, palette):
    # Create the base mosaic graph given physical dimensions and spacing
    G = createMosaicGraph(width_mm, height_mm, spacing_mm)

    # Create a dictionary mapping each node to its coordinates for plotting
    pos = {node: node for node in G.nodes()}

    # Convert dimensions from mm to inches for matplotlib
    fig_w = width_mm / 25.4
    fig_h = height_mm / 25.4
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_subplot(1, 1, 1)
    # Fondo de color claro (puedes cambiar el código hex)
    ax.set_facecolor(palette[0])  # Beige claro elegante
    
    # Check if the graph is planar and get the planar embedding
    is_planar, embedding = check_planarity(G, True)
    if not is_planar:
        raise ValueError("Graph is not planar")

    # Traverse the planar embedding to extract all the faces of the graph
    faces = []
    visited = set()
    for u in embedding:
        for v in embedding[u]:
            if (u, v) not in visited:
                face = embedding.traverse_face(u, v)  # Get the face starting from edge (u, v)
                faces.append(face)
                # Mark all edges of the face as visited to avoid duplication
                for i in range(len(face)):
                    a = face[i]
                    b = face[(i+1) % len(face)]
                    visited.add((a, b))

    # Create a list of sets of edges for each face, used to build the dual graph
    face_edges = []
    for face in faces:
        edges = set()
        for i in range(len(face)):
            u = face[i]
            v = face[(i+1) % len(face)]
            edges.add((u, v))
            edges.add((v, u))  # Ensure edges are undirected
        face_edges.append(edges)

    # Build the dual graph: each face becomes a node,
    # and edges are added between faces that share an edge
    dual_G = nx.Graph()
    for idx1 in range(len(faces)):
        for idx2 in range(idx1 + 1, len(faces)):
            if face_edges[idx1] & face_edges[idx2]:  # Shared edge between faces
                dual_G.add_edge(idx1, idx2)

    # Color the dual graph using a greedy algorithm (since planar graphs are 4-colorable)
    coloring = nx.coloring.greedy_color(dual_G, strategy="largest_first")
    face_colors = [coloring.get(idx, 0) for idx in range(len(faces))]

    # Threshold area to identify "small" faces (~quarter of a cell area)
    threshold = (spacing_mm**2) * 0.3  # Slightly less than 1/4 cell area

    # Reassign certain small orange-colored faces to black
    for idx, face in enumerate(faces):
        if polygonArea(face, pos) < threshold and face_colors[idx] == 1:
            face_colors[idx] = 2  # 2 corresponds to 'black'

    # Define a color map for up to 4 colors
    # color_map = {0: 'beige', 1: 'darkorange', 2: 'black', 3: 'white'}
    color_map = {0: palette[0], 1: palette[1], 2: palette[2], 3: 'white'}


    # Draw each face with its corresponding color
    for idx, face in enumerate(faces):
        x = [pos[node][0] for node in face]
        y = [pos[node][1] for node in face]
        color = color_map[face_colors[idx] % len(color_map)]
        ax.fill(x, y, color=color, alpha=1)

    # Equal aspect ratio and render the plot
    # plt.axis("equal")
    # plt.axis("off")
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    plt.axis("equal")
    plt.show()
    
    
def plotShortestPath(G, pos, start_node, end_node, color, tipo):
    # Find shortest path
    try:
        shortest_path = nx.shortest_path(G, 
                                         source=start_node,
                                         target=end_node,
                                         weight = tipo)
        
        path_edges = list(zip(shortest_path, shortest_path[1:]))
    except nx.NetworkXNoPath:
        print("No path exists between the selected nodes.")
        path_edges = []

    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=color, width=4)        
        # Highlight start and end nodes
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color=color, node_size=10)

        nx.draw_networkx_nodes(G, pos, nodelist=[start_node, end_node], node_color=color, node_size=50)
    
    # plt.axis("equal")
    # plt.axis("off")
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    plt.axis("equal")
    
    plt.show()
    


def main():
    
    # B5 size in mm
    width_mm = 176
    height_mm = 250
    spacing_mm = 10
    
    # Generate the graph
    G = createMosaicGraph(width_mm, height_mm, spacing_mm)
    pos = {node: node for node in G.nodes()}

    # Plot Mosaic
    palette = {0: 'honeydew', 1: 'c', 2: 'black'}
    plotMosaic(width_mm, height_mm, spacing_mm, palette)    
    
    start_node = (25.0, 227.5)
    end_node = (150.0, 27.5)
    color = 'orange'
    tipo = "distance"
    plotShortestPath(G, pos, start_node, end_node, color, tipo)
    
    start_node = (147.5, 230.0)
    end_node = (30.0, 22.5)
    color = 'deeppink'
    tipo = "weight"
    plotShortestPath(G, pos, start_node, end_node, color, tipo)
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig("mosaic_contraportada.pdf", format='pdf', bbox_inches='tight', pad_inches=0, dpi=600)

    # -------------------------------------------------------------------------
    
    # Plot Mosaic
    palette = {0: 'beige', 1: 'darkorange', 2: 'black'}
    plotMosaic(width_mm, height_mm, spacing_mm, palette)    
    
    start_node = (25.0, 227.5)
    end_node = (150.0, 27.5)
    color = 'royalblue'
    tipo = "distance"
    plotShortestPath(G, pos, start_node, end_node, color, tipo)
    
    start_node = (147.5, 230.0)
    end_node = (30.0, 22.5)
    color = 'seagreen'
    tipo = "weight"
    plotShortestPath(G, pos, start_node, end_node, color, tipo)
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig("mosaic_portada.pdf", format='pdf', bbox_inches='tight', pad_inches=0, dpi=600)

    
    
if __name__ == "__main__":
    main()
    
