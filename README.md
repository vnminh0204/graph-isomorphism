* What is the main program that should be called, for both the GI problem and
the #Aut problem?
  - The main program is FINAL_main
  In case you want a version without twin we have FINAL_main_without_twins

* How can you select the instance?
  - In the main method "if __name__ == '__main__':" we have a string variable "directory"
  You can change the directory to input the correct location of file
  Ex: bonus/3130bonus06Aut.gr

* We have option to run without tree processing, GI, Aut graph. However to remove twins we need a new seperate file for that which is "FINAL_main_without_twins.py"