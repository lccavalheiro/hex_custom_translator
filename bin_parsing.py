import argparse
import os
import sys

# Instantiate the parser
parser = argparse.ArgumentParser(description='Names and locations for input and output .hex files')

# Optional positional argument
parser.add_argument('input_hex_file_arg', type=str, nargs='?',
                    help='File name and location of existing firmware .hex')

parser.add_argument('output_hex_file_arg', type=str, nargs='?',
                    help='File name and location to create new .hex')

args = parser.parse_args()

#Check if arguments have been given when calling the script. If yes, use the name of the files given
#If not, try to open and save with default names

#Open existing file
if args.input_hex_file_arg:
    if(not os.path.isfile(args.input_hex_file_arg)):
        sys.exit("No file found. Check the location and name and retry.")
    bin_file = open(args.input_hex_file_arg)  # Open existing .hex file
else:
    if(not (os.path.isfile("firmware.hex"))):
        sys.exit("No file found. Check the location and name and retry.")
    bin_file = open("firmware.hex") #Open existing .hex file

#Make a new file
if args.output_hex_file_arg:
    new_bin = open(args.output_hex_file_arg,"w+")  #Create new .hex file
else:
    new_bin = open("new_binary","w+")  #Create new .hex file

#Create a new string to compose the new file and write to it later on
new_file = ""


new_file += "const char SCB_firmware_file_array[][21] = {\n"

for line in bin_file:
    type_of_line = line[7:9]            #Extract the byte that identifies the line purpose
    if(type_of_line == "00"):           #If the line is memory data type, keep it
        line = line.replace(":","")     #Strips off the colon from the lines
        line = line[0:6]+line[8:len(line)-3]  #Leave only size, address, and data on the line string
        new_file += '{'
        for characters in range(0,len(line),2):  #Add the 0x and comma every 2 character (they represent hexadecimal numbers
            new_file += "0x" + line[characters:characters+2] + ','
        new_file = new_file[:-1] + "},\n"

new_file = new_file[:-2] + "\n};"
new_bin.write(new_file)

print(new_file)
print("Conversion done! New filed save as: " + new_bin.name + ".hex")
bin_file.close()
new_bin.close()
sys.exit("See you next time!")