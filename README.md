# The Sokoban Solver
In this project we introduce a program developed to solve Sokoban game boards using the nuXmv language.

## Input File Format
The input file must be an **.txt** file in an XSB format, where:
- @ warehouse keeper
- \+ warehouse keeper on goal
- $ box
- ∗ box on goal
- \# wall
- . goal
- \- floor

The board must have walls all around it.

## Solver
We present 2 approaches to solve the boards: iterative and not iterative.

### Non Iterative Solver
The code runs using the following format:
```bash
py sokoban.py input_file_name.txt
```
It can also be run by specifying the solver engine (BDD or SAT):

```bash
py sokoban.py input_file_name.txt BDD

```

When "BDD" can be either the BDD or the SAT solver engine.
If using SAT solver its possible to specify a step limit for the run, as the default is 10 steps:

```bash
py sokoban.py input_file_name.txt SAT 50
```

### Iterative Solver
The code solves the board in a furthest-goal manner, meaning it solves the further goals before the close ones.
The code runs using the following format:

```bash
py sokoban.py input_file_name.txt iterative
```


## Outputs
The outputs of the run are saving inside **./outputs/input_file_name** and contain the following files:
- .smv file that was created.
- .out output file that contains the output of the .smv file that was run.
- _LURD.out file containting the LURD format of the run and the execution time.

***NOTE*** : *if using an iterative approach, the .out file will contain only the output for the last solved box.*



## Depositories and Files of the Repository
**Q2_ScreenShots, Q3_ScreenShots, Q4_ScreenShots:** Contain screenshots capturing the command line outputs from part 2,3,4 parts, respectively.

**outputs:** Stores all the output files from the examples executed across various parts. For each example, three specific files are 
generated:
- example.xmv
- example.out
- example_LURD.out

Additionally, for Part 3, output files from both BDD and SAT methodologies are included for each example. Part 4 contains files from both regular (BDD)and interactive runs for comparison.

**.txt example files:** Each example's base files, example.txt, are available in this directory. These files can be downloaded for personal testing and exploration.

**Python files:** The directory includes Python scripts necessary for executing the program. These files are available for download, allowing users to run the program on their own computers.


## Overview of the Roles of the Python Files:

**run_nuxmv.py:** facilitates the execution of the nuXmv model checker tool with options for using either BDD or SAT solvers. Handles process interactions and saves the results to a specified file.

**solver.py:** Orchestrates model checking processes for solving puzzles by integrating board assignment, model generation, LURD formation creation and execution time tracking.

**solver_iterative.py:** Same as solver.py but in an iterative manner.

**LURD_format_creator.py:** Extracts and formats solutions from the output of the nuXmv model checker into a LURD (Left, Up, Right, Down) movement format, where an uppercase letter is a push and an lowercase letter is a move.

**model_generation.py:** Generates the .smv model file for nuXmv by creating a representation of the puzzle board's state and defining the rules for movement and interaction with objects (e.g., boxes and walls). The script specifies initial conditions, transitions, and constraints to enable automated reasoning about possible moves.

**sokoban.py:** Main entry point for the Sokoban puzzle solver application. It reads the board configuration from a .txt file and invokes the appropriate solver according to the input.

