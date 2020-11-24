package model;

public class Node {
    private int color;
    private Boolean fixed;
    private int idx;

    public Node(int color, Boolean fixed, int idx) {
        this.color = color;
        this.fixed = fixed;
        this.idx = idx;
    }

    public int getColor() {
        return color;
    }

    public Boolean getFixed() {
        return fixed;
    }

    public int getIdx() {
        return idx;
    }

    @Override
    public String toString() {
        return "Node{" +
                "color=" + color +
                ", fixed=" + fixed +
                ", idx=" + idx +
                '}';
    }
}
