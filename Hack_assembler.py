""" This is the hack assembler it makes use of the services of parser.py and code_genrator.py
    It generates an equivalent binary code in a '.hack' file of the assmebly code passed
    in a .asm file, and stores it in the same directory as the assembly file.
"""

import hack_parser, code_generator, pathlib

#The assmembler process is divided into stages
#__Preprocess function___

#__STAGE 1__ receiving input and passing it to the parser


#we first read input from the user in form of a file path
print('''Please input the absolute path to file if the file isn\'t in the current directory
Hint: use / delimitter when writing path directory or \\\\ to avoid errors ''')
file = input('\'.asm\' file path here: ')
# Strip extra double quotes incase text input was pasted and not typed
file = file.strip('"')


#initialise symbol table and parser
symbol_table = {'R0':'0', 'R1':'1', 'R2':'2', 'R3':'3', 'R4':'4', 'R5':'5', 'R6':'6',
                'R7':'7', 'R8':'8', 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13,
                'R14':14, 'R15':15, 'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
                'SCREEN':16384, 'KBD':24576, }
line_no = 0
variable_reg = 16
p1 = hack_parser.make_parser(file) #this is the parser used during the first pass

#__STAGE 2__ First Pass

while hack_parser.has_more_lines(p1):
    hack_parser.advance(p1)
    if hack_parser.instructionType(p1) == 'L_INSTRUCTION':
        symbol_table.update({hack_parser.symbol(p1):line_no})
    else: # C or A instruction
        line_no +=1 #increment line for the next command

hack_parser.close_file(p1)
line_no = 0

#__STAGE 3__ Second pass
bin_instr = ''
p2 = hack_parser.make_parser(file)
output_file_path = pathlib.Path(file).with_suffix('.hack')
with open(output_file_path, 'w') as outFile:
    while hack_parser.has_more_lines(p2):
        hack_parser.advance(p2)

        if hack_parser.instructionType(p2) == 'A_INSTRUCTION':
            symbol = hack_parser.symbol(p2)
            if symbol.isdigit(): #A_instruction of type @1234
                bin_instr = bin(int(symbol)).lstrip('0b').zfill(16)
            else: #A_instruction of the form @xxx i.e a LABEL or a variable
                numeric_val= symbol_table.get(symbol, '')
                
                if numeric_val != '': #symbol is in table and has a numeric value
                    bin_instr = bin(int(numeric_val)).lstrip('0b').zfill(16)
                else: #symbol is not in the table hence its a variable
                    bin_instr = bin(variable_reg).lstrip('0b').zfill(16)
                    symbol_table.update({symbol: variable_reg})
                    variable_reg +=1
               
            outFile.write(bin_instr + '\n')
                    
        elif hack_parser.instructionType(p2) == 'C_INSTRUCTION':
            symbolic_dest = hack_parser.dest(p2)
            symbolic_comp = hack_parser.comp(p2)
            symbolic_jump = hack_parser.jump(p2)
            
            bin_dest = code_generator.dest_bin(symbolic_dest)
            bin_comp = code_generator.comp_bin(symbolic_comp)
            bin_jump = code_generator.jump_bin(symbolic_jump)
            bin_instr = '111' + bin_comp + bin_dest + bin_jump

            outFile.write(bin_instr + '\n')


print(f"Assembly complete. Binary code saved to {output_file_path}")

#__STAGE __ assemble result binary code

#__STAGE __ write assembled string to output file




