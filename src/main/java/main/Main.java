package main;

import controller.Controller;

public class Main {

    public static void main(String[] args) {
        System.setProperty("org.graphstream.ui", "swing");

        Controller controller = new Controller();
        controller.setVerbose(true);

        controller.start();

    }
}
