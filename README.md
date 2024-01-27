# Graph Master
## Name
Graph Master.

## Author
Artemiy Shipovalov.
UK MFF, 2024

## Description
The program is used for visual work with graphs.

## Functionality
- Creation of vertices and faces
- Free movement of vertices on the screen plane
- Removal of vertices and faces
- Removal of a whole graph
- Export/Import graph to/from file in JSON format (with saving vertex location)

## Visuals
![visualization.gif](img%2Fvisualization.gif)

## Installation
Before usage install python and module PySide6.
```bash
pip install pyside6
```

## Usage
At the top of the screen is a panel with possible modes of operation. At a particular moment of time exactly 1 mode can be selected. The mode is selected by pressing the button with the name of this mode.
Operating modes:
1. Cursor. In this mode the user can move the graph vertices on the screen by pressing the left mouse button.
2. Add Node. In this mode the user can create a graph node by pressing the left mouse button on a given point.
3. Add Edge. In this mode the user can create edges between vertices. To do this, the user must first click on the first vertex and then on the second vertex, then an edge will be created between them. If the user misses when selecting the first or the second vertex (by clicking on an empty area), the process of vertex selection must be repeated from the beginning.
4. Delete. In this mode the user can delete a vertex or an edge from the graph by clicking on it. When deleting a vertex, all edges incident to it are deleted as well.
On the same panel there is the "Clear Graph" button. It is used to delete the whole graph. If you press this button, a window appears in which you should confirm or cancel the process of deleting the graph.

Program menu:
The "File" menu contains the following buttons:
1. Quit. This button is used to terminate the program.
2. Import. It is used to import a graph saved in JSON format in a text file and then display it on the screen. The graph that was there before is completely erased. If the file format is incorrect, the graph will not be created.
3. Export. Exports the graph to a text file in JSON format.

## JSON file format:
```json
{
	"content_type": "Graph",
	"type_version": version,
	"nodes": [node_1, node_2, ..., node_n],
	"edges": [edge_1, edge_2, ..., edge_m]
}
```
Description:

    content_type - file type
    type_version - file format version
    nodes - graph vertices
    edges - edges of the graph
    
    node_i := [id, x, y, r, name]

    id - vertex id
    x, y - coordinates of the vertex on the plane
    r - vertex radius (by default 25 pixels)
    name - text of the vertex (by default "", i.e. without name)

    edge_i := [id, id_node_1, id_node_2, w, d]

    id - the id of the edge
    id_node_1, id_node_2 - id of the first, second vertex
    w - face weight (by default faces are unweighted)
    d - face direction (by default: 0 - undirected, 1 - towards the second vertex, -1 - towards the first vertex).

## Example
Project has an example, that user can import and play with.

## Roadmap
- Creation of oriented graphs
- Creation of multigraphs
- Setting name and color for a vertex
- Giving color, weight and direction to edges
- Export graph to PNG and SVG formats
- Ability to scale the workspace
- Ability to move around the workspace
- Ability to apply different graph algorithms (BFS, DFS, ...)

## Project for
This project was created as a semester project for the Programming 1 - NPRG030, UK MFF 2024.
