import java.util.*;

class Node {
    HashMap<String, Integer> neighbors;
    int NodeVal;

    public Node(int val) {
        neighbors = new HashMap<>();
        NodeVal = val;
    }

    public HashMap<String, Integer> getNeighbors() {
        return neighbors;
    }

    public int getVal() {
        return NodeVal;
    }

    public void addNeighbor(int NodeVal, int distance) {
        neighbors.put("c" + NodeVal, distance);
    }
}

public class MatrixStructCreator {
    public int[][] generateRandomMatrix(int num) {
        int[][] matrix = new int[num][num];

        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                // generates ranodm num from = 0 - 10
                matrix[i][j] = (int) (Math.random()*11);
            }           
        }
        return matrix;
    }

    public Node getStructure(int[][] matrix) {
        return null;
    }
}
