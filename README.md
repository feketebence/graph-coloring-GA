# Graph Coloring with Genetic Algorithm
<h3>
 Graph coloring with genetic algorithms. The graphs represent an unsolved sudoku, <a href="http://www.sudoku-space.com/hyper-sudoku/">Hyper-Sudoku</a> or <a href="https://en.wikipedia.org/wiki/Nonomino">Nonomino</a> board.
</h3>
<br>

![cover-img](misc/graph-coloring-GA-cover.png?raw=true "Visualization demo of an unfinished 4x4 sudoku graph")

<br>
Graph representation with <a href="https://networkx.org/">NetworkX</a>. <br>
Live graph visualization with <a href="https://graphstream-project.org/">GraphStream</a>. <br>
Communication between GA and visualization component with <a href="https://github.com/zeromq/jeromq">JeroMQ</a> (see <a href="https://zeromq.org/">zeromq.org</a> for more information). <br> 
<hr>

Start with:
<code>$ ./start.sh </code>

<h3>Required libraries</h3>
<ol>
    <li>ZeroMQ <code>$ apt-get install libzmq3-dev </code> </li>
    <li>ZeroMQ Python bindings <code>$ pip install pyzmq </code></li>
    <li>NetworkX <code>$ pip install networkx </code></li>
</ol>  

![cover-img](misc/graph_vizu_v0.1_demo.gif "Visualization demo of an unfinished 9x9 sudoku graph")

