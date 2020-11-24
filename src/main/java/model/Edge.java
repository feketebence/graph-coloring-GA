package model;

public class Edge {
    private int fromNode;
    private int toNode;

    public Edge(int fromNode, int toNode) {
        this.fromNode = fromNode;
        this.toNode = toNode;
    }

    public int getFromNode() {
        return fromNode;
    }

    public int getToNode() {
        return toNode;
    }

    @Override
    public String toString() {
        return "Edge{" +
                "fromNode=" + fromNode +
                ", toNode=" + toNode +
                '}';
    }
}
