# PythonScripts
my python scripts that are not worth a new repo


## LineVisualizer
A line rasterizer written in python and pygame  

**A example line with input x = 10; y = 7:**
![LineVisualizer Screenshot](/src/linevisualizer.png)

## Subprocess Communication
A utility class for communication with a python subprocess which can be any shell command.
Makes it possible to define a callback which is called for every line on the processes stdout and has a function for writing commands to the stdin of the process.  
I use this class in my project [MCWeb](https://github.com/xImAnton/mcweb) for communication with a minecraft server.
