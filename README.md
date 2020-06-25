# SUDOKU GAME

## Requirements:
  1. [Python](https://www.python.org/downloads/release/python-377/)
  2. [Pygame](https://pypi.org/project/pygame/)

## Sudoku GUI ([code](sudoku_gui.py)):

  1. Graphical User Interface that automatically generates a Sudoku Game which can be solved manually or automatically.
  2. Steps to play game:
      i. Select a cell using the mouse, type your answer and press **ENTER**. If the answer is correct it enters the value, else neglects it.
      ii. If you want the machine to solve the game, press **SPACEBAR**.
  3. Difficulty of the game can be changed by varying the **difficulty** parameter in the **generate_sudoku** function.
  
## Sudoku Solver ([code](sudoku_solve.py)):

  1. Solve the sudoku provided as an array inside the code.
  2. Enter the values of the sudoku to be solved in the **array** variable. Enter 0 for unknown values.
  3. Execute the code to obtain the solved sudoku.
  
## Sudoku Generator ([code](sudoku_create.py)):

  1. Creates a random sudoku.
  2. Difficulty can be changed by varying the **difficulty** parameter (Default value = 0.6) in the **generate_sudoku** function.
  
## Drawbacks:

  1. When using the GUI to automatically solving the sudoku, i.e. when you hit SPACEBAR do not use the system until it solves the sudoku completely. 

## Thank you

I hope you found the project useful and interesting. Feel free to contact me if you have any queries or suggestions.

-- [Rohith S P](https://www.linkedin.com/in/rohithsp/)
