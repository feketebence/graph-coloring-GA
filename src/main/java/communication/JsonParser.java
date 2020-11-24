package communication;

import model.Edge;
import model.Model;
import model.Node;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Deserializes a specific JSON formatted string that contains the representation of a  NetworkX graph.
 *
 * JSON Format:
 *        {
 *         'GRID_SIZE': GRID_SIZE: int,
 *         'SQ_GRID': SQ_GRID: int,
 *         'sudoku_graph': {
 *             'nodes':
 *                 [{'color': int, 'fixed': Boolean, 'idx': int}, ...],
 *             'edges':
 *                 [(fromNode:int , toNode: int), ...]
 *             }
 *         }
 */

public class JsonParser {

    /**
     * Processes a part of the JSON string that is related to the nodes of the graph.
     *
     * @param json - JSON formatted string containing every graph related data.
     * @return List of Node objects.  { color: int, fixed: Boolean, idx: int }
     */

    public static ArrayList<Node> extractNodes(String json) {
        Pattern nodePattern = Pattern.compile("(\\{\"color\": [0-9]+, \"fixed\": (false|true), \"idx\": [0-9]+})");
        Matcher matcher = nodePattern.matcher(json);
        ArrayList<Node> nodes = new ArrayList<>();

        while (matcher.find()) {
            String nodeString = matcher.group(0);

            nodeString = nodeString
                    .replace(" ", "")
                    .replace("}", "")
                    .replace("{\"color\":", "")
                    .replace("\"fixed\":", "")
                    .replace("\"idx\":", "");

            String[] splitString = nodeString.split(",");
            int color = Integer.parseInt(splitString[0]);
            Boolean fixed = Boolean.getBoolean(splitString[1]);
            int idx = Integer.parseInt(splitString[2]);

            nodes.add(new Node(color, fixed, idx));
        }

        return nodes;
    }

    /**
     * Processes a part of the JSON string that is related to the edges of the graph.
     *
     * @param json - JSON formatted string containing every graph related data.
     * @return List of Edge objects.  { fromNode: int, toNode: int }
     */

    public static ArrayList<Edge> extractEdges(String json) {

        Pattern edgePattern = Pattern.compile("(\\[[0-9]+, [0-9]+])+(,|)( |)");
        Matcher edgeMatcher = edgePattern.matcher(json);
        ArrayList<Edge> edges = new ArrayList<>();

        while (edgeMatcher.find()) {
            String edgeString = edgeMatcher.group(0);

            edgeString = edgeString
                    .replace("],", "")
                    .replace("]", "")
                    .replace("[", "");

            String[] splitString = edgeString.replace(" ", "").split(",");
            int fromNode = Integer.parseInt(splitString[0]);
            int toNode = Integer.parseInt(splitString[1]);

            edges.add(new Edge(fromNode, toNode));
        }

        return edges;
    }

    /**
     * Processes a part of the JSON string that is related to the size of the sudoku board.
     *
     * @param json - JSON formatted string containing every graph related data.
     * @return The size of the sudoku grid.
     */

    public static int extractGridSize(String json) {
        Pattern gridSizePattern = Pattern.compile("\"GRID_SIZE\": [0-9]+");
        Matcher matcher = gridSizePattern.matcher(json);

        if (matcher.find()) {
            String matchedStr = matcher.group(0);
            matchedStr = matchedStr.split(" ")[1];

            return Integer.parseInt(matchedStr);
        } else {
            return -1;
        }
    }

    /**
     * Processes a part of the JSON string that is related to the size of the smaller sub-grids of the sudoku board.
     *
     * @param json JSON formatted string containing every graph related data.
     * @return The size of the sub-grids.
     */
    public static int extractSquareSize(String json) {
        Pattern gridSizePattern = Pattern.compile("\"SQ_GRID\": [0-9]+");
        Matcher matcher = gridSizePattern.matcher(json);

        if (matcher.find()) {
            String matchedStr = matcher.group(0);
            matchedStr = matchedStr.split(" ")[1];

            return Integer.parseInt(matchedStr);
        } else {
            return -1;
        }
    }

    /**
     * Creates a Model object from based on the JSON formatted input string.
     * @param json JSON formatted string containing every graph related data.
     * @return A Model representing the sudoku board as a graph.
     */

    public static Model buildSudokuData(String json) {
        // build model from client request
        ArrayList<Node> nodes = JsonParser.extractNodes(json);
        ArrayList<Edge> edges = JsonParser.extractEdges(json);
        int gridSize = JsonParser.extractGridSize(json);
        int sqSize = JsonParser.extractSquareSize(json);

        return new Model(gridSize, sqSize, nodes, edges);
    }
}
