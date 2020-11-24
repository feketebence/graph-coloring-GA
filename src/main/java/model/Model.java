package model;

import java.util.List;

/**
 * This object contains everything that is needed to visualize a sudoku graph.
 */

public class Model {
    private int gridSize;
    private int sqGrid;
    private List<Node> nodes;
    private List<Edge> edges;

    public Model(int gridSize, int sqGrid, List<Node> nodes, List<Edge> edges) {
        this.gridSize = gridSize;
        this.sqGrid = sqGrid;
        this.nodes = nodes;
        this.edges = edges;
    }

    @Override
    public String toString() {
        return "Model{\n" +
                "gridSize=" + gridSize + ",\n" +
                "sqGrid=" + sqGrid + ",\n" +
                "nodes=\n" + toStringNodes() + "\n" +
                "edges=\n" + toStringEdges() +
                '}';
    }

    public String toStringNodes() {
        StringBuilder returnVal = new StringBuilder();
        for(Node node : this.nodes) {
            returnVal.append(node).append("\n");
        }

        return returnVal.toString();
    }

    public String toStringEdges() {
        StringBuilder returnVal = new StringBuilder();
        for(Edge edge : this.edges) {
            returnVal.append(edge).append("\n");
        }

        return returnVal.toString();
    }

    public int getGridSize() {
        return gridSize;
    }

    public int getSqGrid() {
        return sqGrid;
    }

    public List<Node> getNodes() {
        return nodes;
    }

    public List<Edge> getEdges() {
        return edges;
    }

    public void setGridSize(int gridSize) {
        this.gridSize = gridSize;
    }

    public void setSqGrid(int sqGrid) {
        this.sqGrid = sqGrid;
    }

    public void setNodes(List<Node> nodes) {
        this.nodes = nodes;
    }

    public void setEdges(List<Edge> edges) {
        this.edges = edges;
    }
}
