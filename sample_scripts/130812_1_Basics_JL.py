"""
Sample 1 : A barebones script
Loading : 1)Referencing folder or 2)importing ur.dll
"""

#1) Import 
import urscript as urs
import comm 


#2) Create a command
command = urs.popup("hi students", "title is title")

#3) Create a program
my_program = urs.create_function('main', [command])
print my_program

#4) Send the program
comm.send_script(my_program, "192.168.10.13")