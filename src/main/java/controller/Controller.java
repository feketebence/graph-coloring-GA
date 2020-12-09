package controller;

import communication.Channel;
import communication.JsonParser;
import model.Edge;
import model.Model;
import model.Node;
import org.graphstream.graph.Element;
import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Controller {
    private Model model;
//    private View view;

    private boolean isVerbose;

    private Graph graph = getSingleGraph();

    public Controller() {
        this.model = new Model(0, 0, new ArrayList<>(), new ArrayList<>());
//        this.view = new View(this.model);
        this.isVerbose = true;
    }

    public void setVerbose(boolean verbose) {
        isVerbose = verbose;
    }

    public void start() {

        String address = "tcp://*:5556";
        Channel channelToClient = new Channel(address);
        channelToClient.setVerbose(false);
        int msgCount = 0;

        channelToClient.bind();

        this.graph.display();
        this.setStyle();


        if(isVerbose) {
            System.out.println("Server started! Listening on " + address);
        }

        while (!Thread.currentThread().isInterrupted()) {

            channelToClient.listenForMessage();

            // handle the 'END' message, basically a signal from the graph-generator process signaling that the task is finished (final solution is found)
            if(channelToClient.getReceivedMessage().equals("END")) {
                channelToClient.sendResponse("Got END signal, server is going down.");
                break;
            }

            channelToClient.sendResponse("Got message nr. " + ++msgCount);
            String json = channelToClient.getReceivedMessage();

            if(isVerbose) {
                System.out.println("Received message: \n" + json);
            }

            System.out.println("Got graph nr. " + msgCount);

            Model generatedModel = JsonParser.buildSudokuData(json);
            this.model.setGridSize(generatedModel.getGridSize());
            this.model.setSqGrid(generatedModel.getSqGrid());
            this.model.setNodes(generatedModel.getNodes());
            this.model.setEdges(generatedModel.getEdges());

            addNodes();
            addEdges();

            System.out.println("Finished visualizing graph nr. " + msgCount + "\n");
            mockProcessing(3000);

        }

        System.out.println("Done.");

    }

    private void addNodes() {
        System.out.println("Adding nodes...");

        for(Node node : this.model.getNodes()) {
            Element addedNode = graph.addNode(String.valueOf(node.getIdx()));
            addedNode.setAttribute("color", node.getColor());
            addedNode.setAttribute("fixed", node.getFixed());
            addedNode.setAttribute("ui.label", node.getIdx());

            mockProcessing(5);

            addedNode.setAttribute("ui.class", defineColorClass(node.getColor()));
            mockProcessing(5);
        }
    }

    private void addEdges() {
        System.out.println("Adding edges...");

        for(Edge edge : this.model.getEdges()) {
            org.graphstream.graph.Edge addedEdge = graph.addEdge(edge.getFromNode() + "-" + edge.getToNode(), edge.getFromNode(), edge.getToNode());
            mockProcessing(10);

            //check for same color conflict
            int node0Value = (Integer) addedEdge.getNode0().getAttribute("color");
            int node1Value = (Integer) addedEdge.getNode1().getAttribute("color");

            if (node0Value == node1Value) {
                addedEdge.setAttribute("ui.class", "conflict");
            }
        }
    }

    private Graph getSingleGraph() {
        graph = new SingleGraph("SudokuGraph");
        graph.setAutoCreate(true);
        graph.setStrict(false);

        return graph;
    }

    private void setStyle() {
        // the correct way, but cannnot create the jar properly and throws java.io.FileNotFoundException: src/main/resources/stylesheet.css
        // therefore I use the explicit style string as a fallback

        StringBuilder stylesheet = new StringBuilder();

        //the ugly way as a fallback
        String stylesheetManual = "node {\n" +
                "\tfill-color: rgb(0,0,0);\n" +
                "\ttext-alignment: under;\n" +
                "\tsize: 20px;\n" +
                "\tstroke-mode: plain;\n" +
                "\tstroke-color: #000;\n" +
                "\ttext-size: 15px;\n" +
                "}\n" +
                "\n" +
                "node.zero {\n" +
                "\tfill-color: rgb(0,0,0);\n" +
                "}\n" +
                "\n" +
                "node.one {\n" +
                "\tfill-color: rgb(166,206,227);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.two {\n" +
                "\tfill-color: rgb(31,120,180);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.three {\n" +
                "\tfill-color: rgb(178,223,138);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.four {\n" +
                "\tfill-color: rgb(51,160,44);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.five {\n" +
                "\tfill-color: rgb(251,154,153);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.six {\n" +
                "\tfill-color: rgb(227,26,28);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.seven {\n" +
                "\tfill-color: rgb(253,191,111);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.eight {\n" +
                "\tfill-color: rgb(255,127,0);\n" +
                "}\n" +
                "\n" +
                "\n" +
                "node.nine {\n" +
                "\tfill-color: rgb(202,178,214);\n" +
                "}\n" +
                "\n" +
                "edge {\n" +
                "    fill-color: rgb(0, 0, 0);\n" +
                "    shape: cubic-curve;\n" +
                "}\n" +
                "\n" +
                "\n" +
                "edge.conflict {\n" +
                "    fill-color: rgb(255, 15, 55);\n" +
                "}";

        try {
            File cssFile = new File("src/main/resources/stylesheet.css");
            Scanner scanner = new Scanner(cssFile);

            while(scanner.hasNextLine()) {
                stylesheet.append(scanner.nextLine());
            }

            scanner.close();
            this.graph.setAttribute("ui.stylesheet", stylesheet.toString());

        } catch (FileNotFoundException e) {
            System.out.println("File src/main/resources/stylesheet.css not found");
//            e.printStackTrace();

            System.out.println("Using explicit stylesheet from source code");
            this.graph.setAttribute("ui.stylesheet", stylesheetManual);
        }




//
//        this.graph.setAttribute("ui.stylesheet", stylesheet);
    }

    private String defineColorClass(int colorIdx) {
        if (colorIdx == 1) {
            return "one";
        } else if (colorIdx == 2) {
            return "two";
        } else if (colorIdx == 3) {
            return "three";
        } else if (colorIdx == 4) {
            return "four";
        } else if (colorIdx == 5) {
            return "five";
        } else if (colorIdx == 6) {
            return "six";
        } else if (colorIdx == 7) {
            return "seven";
        } else if (colorIdx == 8) {
            return "eight";
        } else if (colorIdx == 9) {
            return "nine";
        } else {
            return "zero";
        }
    }

    private void mockProcessing(long amountOfTime) {
        try {
//            if(isVerbose) {
//                System.out.println("Processing... (sleeping for " + amountOfTime + "ms)");
//            }
            Thread.sleep(amountOfTime);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
