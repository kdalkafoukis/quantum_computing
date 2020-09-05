# Generate quantum state from an array of numbers

## Description
Given an array of numbers we want to generate this state in a quantum computer.  

It's state preparation for problems such as finding the minimum and many other problems.

## example

### input

- python array `[3, 8, 5, 15, 2]`

### output 

- `(0.4472135955+0j)|0000011> + (0.4472135955+0j)|0011000> + (0.4472135955+0j)|0100101> + (0.4472135955+0j)|0111111> + (0.4472135955+0j)|1000010>`

- the first 3 bits are the position bits  
- the other 4 bits are for the number value

## architecture

1. handling input
2. shifting quantum input  
3. create unitary operator to transform the initial state  
4. handling output

