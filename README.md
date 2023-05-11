## Tomasulo's algorithm

[Tomasulo's algorithm](https://en.wikipedia.org/wiki/Tomasulo%27s_algorithm) is a computer architecture hardware algorithm for dynamic scheduling of instructions that allows out-of-order execution and enables more efficient use of multiple execution units. The major innovations of Tomasulo’s algorithm include register renaming in hardware, reservation stations for all execution units, and a common data bus (CDB) on which computed values broadcast to all reservation stations that may need them. These developments allow for improved parallel execution of instructions that would otherwise stall under the use of scoreboarding or other earlier algorithms.

## 💻 Architecture

<div align="center"> 
    <img align="center" src="https://cdn.discordapp.com/attachments/1106243014571085845/1106243025308491886/image.png"/>
</div>

-----------------------------
### 👨‍💻 Valid commands
- ***LW, SW, ADD, SUB, MUL, DIV***
    - **Cycles per instruction -** **LW:** 2, **SW:** 2, **ADD:** 2, **SUB:** 2, **MUL:** 10, **DIV:** 40


-----------------------------
#### Bibliography

- David A. Patterson and John L. Hennessy. 2013. Computer Organization and Design, Fifth Edition: The Hardware/Software Interface (5th. ed.). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA.
