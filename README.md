# ScoreBoard-Simulator
Computer Architecture with User Interface - Scoreboard Algorithm Simulator

## Main Functionality Description
### Basic Functions
This system is a simulation system for scoreboarding algorithm, implementing the required mandatory and optional features, including instruction issue, operand reading, execution, and writeback simulation; viewing instruction status table, functional unit status table, and result register status table; and providing a visual interface.<br>

The specific functionalities are as follows:<br>

(1) Implementation of the scoreboarding algorithm<br>
  For a given set of instructions, the system can dynamically schedule the instructions through the stages of instruction issue, operand reading, execution, and writeback.<br>
(2) Viewing instruction status table, functional unit status table, and result register status table<br>
  For each clock cycle during dynamic scheduling, the system calculates and saves the values in the instruction status table, functional unit status table, and result register status table based on the algorithm.
(3) Visual interface<br>
  Design a reasonable, concise, neat, and comprehensive visual interface to better demonstrate the execution process of the scoreboarding algorithm through a user graphical interface.<br>
(4) Simple and secure control methods<br>
  The system implements flexible cycle selection functionality for convenient and simple control. It provides control interfaces such as "Execute One Cycle," "Step Back One Cycle," "Execute Until a Certain Cycle," "Execute Until the End," and "Reset." After loading the program, users can freely view the contents of each cycle.

Considering the logical relationships between control buttons, certain restrictions are in place. For example, before importing a program, the "Export Results" and "Execute" buttons are disabled. Similarly, the "Step Back" button is disabled when the algorithm has not started executing.

To prevent user errors, the system ensures control button safety by enabling or disabling their interactivity. For instance, when a program has not been imported, buttons such as "Export Results," "Reset," and "Execute One Cycle" are set to a non-interactive state. Only after the program has been loaded, these buttons become available. The same principle applies to similar situations. By reducing the likelihood of user errors, the system greatly enhances operational safety.
