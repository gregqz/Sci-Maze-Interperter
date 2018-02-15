# Sci-Maze-Interperter
An Maze-Interperter with additional parts that make it slower, but more useful; based off of Maze-Interperter-V2 https://github.com/olls/maze-interpreter-v2 ; It should be compatible with http://esolangs.org/wiki/Maze.

## Changes
The changes I have made are extensive, so it shouldn't be used in any serious manner.
* Now supports arbitrary precision in mathematics
* Implemented two new objects: The busstop and switchgate
* Outputs what each car is carrying as well as the driver in debug mode

## Busstops
The largest change is the implementation of busstops which trigger an operation given to the cars.
The busstop is implemented through `::`

| Operator | Effect                                                                           |
|:-------- |:-------------------------------------------------------------------------------- |
| `;-`     | top passenger - bench value                                                      |
| `;+`     | top passenger + bench value                                                      |
| `;*`     | top passenger * bench value                                                      |
| `;/`     | top passenger / bench value                                                      |
| `;$`     | let passenger on (value of bench append to passengers)                           |
| `;s`     | Switch driver with top passenger                                                 |
| `;c`     | Clone driver (value of car append to passengers)                                 |
| `;k`     | Kill top passenger (remove top passenger)                                        |
| `;l`     | Let off top passenger (value of bench = top passenger, and removed)              |
| `;h`     | Person on Bench hijacks car (value of bench = value of car)                      |
| `;w`     | The Driver takes over the Switchgate                                             |
| `;u`     | The Switchgate operator takes over the Car                                       |
| `;x`     | The driver checks into the X hotel                                               |
| `;y`     | The driver checks into the Y hotel                                               |
| `;t`     | The driver checks into the t hotel                                               |
| `;p`     | Outputs a datafile containing the x,y,t hotels data                              |

##Functional Changes
There are new functional operators which concern the use of the switchgate, an number which controls all of the switchgate functions in the maze within an if-then function
| Operator | Effect                                                                                   |
|:-------- |:---------------------------------------------------------------------------------------- |
| ` @`     | Instead of a number, use an at symbol to refer to the driver in the following functions  |
| `!@`     | Not equal to switchgate    |
| `=@`     | Is equal to switchgate     |
| `>@`     | Is Greater Than switchgate |
| `<@`     | Is Less Than switchgate    |
## Examples
There is a program called busstop.mz which demonstrates some of this new capability
## Run
To run a program with this interperter pass the file as a argument to main.py
`python3 main.py file`
