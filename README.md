## Thesis Cover Mosaic Generator

A small Python project to generate artistic mosaic covers for thesis dissertations using network graphs and planar embeddings.

### Features

* **Configurable size**: Define the cover dimensions in millimeters (e.g., B5 size: 176×250 mm).
* **Adjustable grid spacing**: Control the density of the mosaic pattern.
* **Planar mosaic design**: Uses a quarter-grid subdivision and diagonal connections to create an intricate design that remains planar.
* **Dual-graph coloring**: Automatically colors each region using a greedy 4-coloring algorithm, with options to highlight small areas in a different color.
* **Shortest-path overlays**: Compute and overlay shortest paths on the mosaic, based on either geometric distance or custom edge weights.
* **Custom palettes**: Easily swap between color palettes for the background, mosaic regions, and path highlights.
* **PDF export**: Save high-resolution PDF versions of both front and back cover designs.

### Dependencies

* Python 3.7+
* [NetworkX](https://networkx.org/) for graph creation and algorithms
* [Matplotlib](https://matplotlib.org/) for drawing and exporting graphics

Install dependencies via pip:

```bash
pip install networkx matplotlib
```

### Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/thesis-cover-mosaic.git
   cd thesis-cover-mosaic
   ```

2. **Run the script**

   ```bash
   python main.py
   ```

   This will generate two PDF files in the project root:

   * `mosaic_contraportada.pdf`: Back cover design
   * `mosaic_portada.pdf`: Front cover design

3. **Customize parameters**

   In `main.py`, adjust the following variables:

   ```python
   # Dimensions (in mm)
   width_mm = 176
   height_mm = 250
   spacing_mm = 10

   # Color palettes
   palette_back = {0: 'honeydew', 1: 'c', 2: 'black'}
   palette_front = {0: 'beige', 1: 'darkorange', 2: 'black'}

   # Shortest-path examples (modify as desired)
   start_node = (25.0, 227.5)
   end_node = (150.0, 27.5)
   ```

4. **Integrate into LaTeX**

   Include the generated PDFs in your dissertation template:

   ```latex
   \includepdf[pages=-,width=\textwidth]{mosaic_portada.pdf}
   ```

### How It Works

1. **Graph Construction**: The canvas is divided into a regular grid of cells, each further subdivided into a 4×4 quarter-grid. Nodes and internal diagonal edges are added within every other cell to form the mosaic pattern.
2. **Bridge Edges**: Additional edges connect adjacent cells, ensuring global connectivity while preserving planarity.
3. **Planarity Check & Embedding**: The code verifies graph planarity and extracts a planar embedding to enumerate all faces (regions).
4. **Dual Graph Coloring**: A dual graph is built where each face is a node, and edges indicate shared boundaries. A greedy coloring assigns each region one of four colors.
5. **Rendering**: Regions are filled with leaf colors using Matplotlib. Shortest-paths between specified nodes can be overlaid, based on geometric distance or random weights.


---

**Enjoy designing your thesis cover! Feel free to open issues or pull requests.**

