# ScoreBoard-Simulator
Computer Architecture with User Interface - Scoreboard Algorithm Simulator

## Main Functionality Description
### Basic Functions
This system is a simulation system for scoreboarding algorithm, implementing the required mandatory and optional features, including instruction issue, operand reading, execution, and writeback simulation; viewing instruction status table, functional unit status table, and result register status table; and providing a visual interface.<br>

The specific functionalities are as follows:<br>

#### (1) Implementation of the scoreboarding algorithm<br>
  For a given set of instructions, the system can dynamically schedule the instructions through the stages of instruction issue, operand reading, execution, and writeback.<br>
#### (2) Viewing instruction status table, functional unit status table, and result register status table<br>
  For each clock cycle during dynamic scheduling, the system calculates and saves the values in the instruction status table, functional unit status table, and result register status table based on the algorithm.
#### (3) Visual interface<br>
  Design a reasonable, concise, neat, and comprehensive visual interface to better demonstrate the execution process of the scoreboarding algorithm through a user graphical interface.<br>
#### (4) Simple and secure control methods<br>
  The system implements flexible cycle selection functionality for convenient and simple control. It provides control interfaces such as "Execute One Cycle," "Step Back One Cycle," "Execute Until a Certain Cycle," "Execute Until the End," and "Reset." After loading the program, users can freely view the contents of each cycle.

  Considering the logical relationships between control buttons, certain restrictions are in place. For example, before importing a program, the "Export Results" and "Execute" buttons are disabled. Similarly, the "Step Back" button is disabled when the algorithm has not started executing.

  To prevent user errors, the system ensures control button safety by enabling or disabling their interactivity. For instance, when a program has not been imported, buttons such as "Export Results," "Reset," and "Execute One Cycle" are set to a non-interactive state. Only after the program has been loaded, these buttons become available. The same principle applies to similar situations. By reducing the likelihood of user errors, the system greatly enhances operational safety.

### Extended Functions
  In addition to the aforementioned features, the system also implements the following innovative functions to make it more comprehensive:

#### (1) Instruction File Import Function
  In typical scoreboarding algorithm simulators, instructions are selected and set by users through a limited number of instruction selection boxes provided in the graphical interface.<br>
  To overcome this limitation, the system allows instructions to be loaded by importing a file. Instructions are written in a text file and then loaded into the program through the file import process. This method removes the restriction on the number of instructions, enabling the system to simulate an arbitrary number of instructions and expanding its functionality.
#### (2) Instruction Checking and Error Message Output
  After importing the file, the system parses and checks the instructions. If any errors are detected, a prompt window will appear to alert the user to make corrections. The encountered error messages are also stored in a text file for users to modify the instructions.<br>
  The system can detect errors including syntax errors, unknown instruction operand errors, incorrect number of instruction operands, and register usage errors, covering the basic scenarios where errors might occur. This functionality ensures the correctness of the input program, guarantees the algorithm receives valid input, and enhances the system's robustness. Please refer to the system functionality module for specific syntax specifications.
#### (3) Pre-execution of Instructions
  A crucial requirement in scoreboarding simulator design is the ability to freely select any cycle of the scoreboarding algorithm for viewing. However, if the execution process is synchronized with the graphical interface, meaning that only after executing one cycle can the results be displayed for that cycle, operations like stepping back one cycle or jumping to a specific cycle cannot be achieved.<br>
  To address this issue, the system introduces the concept of pre-executing instructions. During program import, the system dynamically schedules and executes the program using the scoreboarding algorithm. It saves the information of the instruction status table, functional unit status table, and result register status table for each cycle in an array structure. When visualizing the execution process later on, the system directly retrieves and displays the corresponding status of the instruction status table, functional unit status table, and result register status table by using the clock cycle as an index. The introduction of pre-execution of instructions makes the control of the system more convenient.
#### (4) Scrollable Instruction Status Table Design
  In typical scoreboarding algorithm simulators, the instruction status table is fixed and displays the status of all instructions at once, which limits the number of instructions that can be displayed. The system adopts a scrollable instruction status table design, where the table is fixed to display three rows, but the content displayed changes as the scoreboarding algorithm executes. It only shows the status of the last three instructions issued. This avoids the need to adjust the length of the instruction status table based on the number of instructions, maintaining a clean and consistent system interface.
#### (5) Instruction Status Table Result Export Function
  The instruction status table contains important information about the execution of each instruction, such as which stage is completed in which clock cycle. In the case of a scrollable instruction status table, to obtain the instruction status table information for all instructions, the system provides an instruction status table result export function. This allows exporting the information of the instruction status table to a text file for reference, ensuring the completeness of the system's functionality.
#### (6) Other Functions
  In addition to the above functionalities, the system also provides buttons for setting the error log and run result output paths, as well as a help module, further enriching the system's content.
