### Team members:
- Vo Nhat Minh
- Tran Duc Duc
- Salih Eren Yücetürk
- Jelle Boon

# I. Abstractions - Project Overview:

The focus of this project is on practical implementations of algorithms for the notorious graph isomorphism problem, a problem that is still open with respect to its computational complexity which puts the problem closer to P than being NP-hard. Algorithms that can decide if two given
input graphs are isomorphic or not, or algorithms that detect the (number of) symmetries
of a given graph, are useful in many practical applications: Mathematical Optimization,
Computational Biology, Fingerprints, etc.

# II. Installation:
## What is the main program that should be called, for both the GI problem and the #Aut problem?
  - The main program is FINAL_main
  In case you want a version without twin we have FINAL_main_without_twins

## How can you select the instance?
  - In the main method "if __name__ == '__main__':" we have a string variable "directory"
  You can change the directory to input the correct location of file
  Ex: bonus/3130bonus06Aut.gr

## We have option to run without tree processing, GI, Aut graph.
