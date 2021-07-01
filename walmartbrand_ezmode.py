#need to specify python3 when running 
import os
import subprocess
import glob
import sys
import numpy as np
import pdb
sublist_number = 800
def exit_ezmode():

	sys.exit('\nBye!\n')

def make_lists():
	global sublist_number

        # Get the name of the list
	list_name = glob.glob('valdLinelist-4800-5300.txt')

        # Get the number of lines in the list
	list_size = subprocess.run(['wc', '-l', list_name], stdout=subprocess.PIPE).stdout.decode('utf-8')
	list_size = int(list_size.split(' ')[0])
        # Generate the request lists
	starting_line = 1	
	request_number = 1
	pdb.set_trace()
	while starting_line <= list_size:
                # Create the head (if this is the first request list)
		if starting_line == 1:
			os.system('head -'+str(sublist_number)+' '+list_name+' > _spec'+str(request_number)+'.txt')

                # Create the tail (for subsequent request lists)
		else:
			os.system('tail -n +'+str(starting_line)+' '+list_name+' | head -'+str(sublist_number)+' > _spec'+str(request_number)+'.txt')

                # Update the starting line and request number by adding 800
		if request_number == 1:
			starting_line = starting_line + 808
		else: 
			starting_line = starting_line + sublist_number
			request_number = request_number + 1

        # Print the master list size and the summed request list sizes for comparison
	print('Master List Size: '+str(list_size)+'\n')	
	os.system('wc -l _spec*.txt')
# Commands
while 1 != 0:

        # Enter command here
	command = input('Input a command (type \'commands\' for a list of commands): ')
        # make lists
	if command == 'make lists':

        	make_lists()

        # exit
	if command == 'exit':

		exit_ezmode()
