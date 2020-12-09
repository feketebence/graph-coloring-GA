#!/bin/bash
x-terminal-emulator -e python src/main/python/GA_sudoku_graph/GA_graph_coloring.py
x-terminal-emulator -e java -jar target/graph-coloring-GA-1.0-SNAPSHOT-uber.jar
echo 'Finished'