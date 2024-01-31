# Graph Master
## Name
Graph Master.

## Author
Artemiy Shipovalov.
UK MFF, 2024

## Description
The program is used for visual work with graphs.

## Functionality
- Creation of nodes and edges
- Free movement of nodes on the screen plane
- Removal of nodes and edges
- Removal of a whole graph
- Export/Import graph to/from file in JSON format (with saving node location)

## Visuals
![visualization.gif](img%2Fvisualization.gif)

## Installation
Before usage install python and module [PySide6](https://doc.qt.io/qtforpython-6/).
```bash
pip install pyside6
```

## Usage
Launch **app.py**.

At the top of the screen is a panel with possible modes of operation. At a particular moment of time exactly 1 mode can be selected. The mode is selected by pressing the button with the name of this mode.
Operating modes:
1. **Cursor**. In this mode the user can move the graph nodes on the screen by pressing and then holding the left mouse button.
2. **Add Node**. In this mode the user can create a graph node by pressing the left mouse button on a given point.
3. **Add Edge**. In this mode the user can create edges between nodes. To do this, the user must first click with the left mouse button on the first node and then on the second node, then an edge will be created between them. If the user misses when selecting the first or the second node (by clicking on an empty area), the process of node selection must be repeated from the beginning.
4. **Delete**. In this mode the user can delete a node or an edge from the graph by clicking on it with the left mouse button. When deleting a node, all edges incident to it are deleted as well.

On the same panel there is the "**Clear Graph**" button. It is used to delete the whole graph. If you press this button, a window appears in which you should confirm or cancel the process of deleting the graph.

Program menu:

The "**File**" menu contains the following buttons:
1. **Quit**. This button is used to terminate the program.
2. **Import**. It is used to import a graph saved in JSON format in a .graph file and then display it on the screen. The graph that was there before is completely erased. If the file format is incorrect, the graph will not be created.
3. **Export**. Exports the graph to a .graph file in JSON format.

## JSON file format:
Files have an extension .graph.
Data is saved in text mode.
```json
{
	"content_type": "Graph",
	"type_version": "version",
	"nodes": ["node_1", "node_2", "...", "node_n"],
	"edges": ["edge_1", "edge_2", "...", "edge_m"]
}
```
Description:

    content_type - file type
    type_version - file format version
    nodes - graph nodes
    edges - graph edges
    
    node_i := [id, x, y, r, name]

    id - node id
    x, y - coordinates of the node on the plane
    r - node radius (by default 25 pixels)
    name - text of the node (by default "", i.e. without name)

    edge_i := [id, id_node_1, id_node_2, w, d]

    id - the id of the edge
    id_node_1, id_node_2 - id of the first, second node
    w - edge weight (by default edges are unweighted)
    d - edge direction (by default: 0 - undirected, 1 - towards the second node, -1 - towards the first node).

## Example
Project has an example, that user can import and play with.

## Programmer's description:
Used module is PySide6. Scene for drawing graph - QGraphicsScene.
Created own classes for buttons, nodes, edges, graph.
Class Graph stores all nodes and edges and manages work with them.

## Roadmap
- Creation of oriented graphs
- Creation of multigraphs
- Setting name and color for a node
- Giving color, weight and direction to edges
- Export graph to PNG and SVG formats
- Ability to scale the workspace
- Ability to move around the workspace
- Ability to apply different graph algorithms (BFS, DFS, ...)
- Optimize selecting and deleting nodes/edges

## Project for
This project was created as a semester project for the Programming 1 - NPRG030, UK MFF 2024.

## License
This project is licensed under the terms of the MIT license.
