package view;

import model.Model;
import model.Node;
import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;

/**
 * This class is responsible for displaying the graph.
 *
 * Currently unused.
 */

public class View {
    private Model model;
    private Graph graph;

    public View(Model model) {
        this.model = model;
        this.graph = new SingleGraph("Sudoku Graph " + model.getGridSize() + "x" + model.getGridSize());
        this.graph.setStrict(false);
        this.graph.setAutoCreate(true);
    }

    public void setModel(Model model) {
        this.model = model;
        System.out.println("model changed");
    }

    public void display() {
        System.out.println("The model:");
        System.out.println(this.model.toString());

        this.graph.display();

        // add nodes
        for(Node node : this.model.getNodes()) {
            System.out.println("Node added");
            graph.addNode(String.valueOf(node.getIdx()));
        }

        // add edges
        //...
    }


}
