## Tomasulo's algorithm

[Tomasulo's algorithm](https://en.wikipedia.org/wiki/Tomasulo%27s_algorithm) is a computer architecture hardware algorithm for dynamic scheduling of instructions that allows out-of-order execution and enables more efficient use of multiple execution units. The major innovations of Tomasulo’s algorithm include register renaming in hardware, reservation stations for all execution units, and a common data bus (CDB) on which computed values broadcast to all reservation stations that may need them. These developments allow for improved parallel execution of instructions that would otherwise stall under the use of scoreboarding or other earlier algorithms.

## 💻 Architecture

<div align="center"> 
    <img align="center" src="https://cdn.discordapp.com/attachments/1094515229578235967/1103276856431624245/A49zZDoYsrZ8AAAAAElFTkSuQmCC.png"/>
</div>

-----------------------------

#### Bibliography

- David A. Patterson and John L. Hennessy. 2013. Computer Organization and Design, Fifth Edition: The Hardware/Software Interface (5th. ed.). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA.
