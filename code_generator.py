""" This is the code generator, it reads from a static file containing the binary
    equivalent of the symbolic Hack assembly instruction passed to it and then
    and returns the equivalent binary instructions
    
"""

destAndJump_file = "C:/Users/Chibueze/Documents/Pyprograms/Nand2Tetris_Assembler/destAndJumpBin.txt"
ALU_bin_file = "C:/Users/Chibueze/Documents/Pyprograms/Nand2Tetris_Assembler/ALU_bin.txt"

def dest_bin(asm_dest:str):
    """ Goes through the destAndJump file and searchs for the equivalent
        binary instruction to the dest assembly instruction.
    """
    binary = ''
    if asm_dest =='':
        binary = '000'
        return binary
    
    with open(destAndJump_file) as DG:
        while True:
            
            instruction = DG.readline()
            if instruction: #not EOF if instruction != ''
                instruction = instruction.strip()
                if instruction.startswith(asm_dest):
                    binary = instruction.split(' ')[1]
                    return binary
            else: #end of file reached
                break
            
        if binary == '':
            raise Exception(f'Invalid destination command - {asm_dest}. Any combination of A, M or D')


def jump_bin(asm_jump:str):
    """ Goes through the destAndJump file and searchs for the equivalent
        binary instruction of the jump assembly instruction.
    """
    binary = ''
    if asm_jump =='':
        binary = '000'
        return binary
    
    with open(destAndJump_file) as DG: #remeber to put the actual path to the file in the directory
        while True:
            
            instruction = DG.readline()
            if instruction: #not EOF if instruction != ''
                instruction = instruction.strip()
                if instruction.startswith(asm_jump):
                    binary = instruction.split(' ')[1]
                    return binary
            else: #end of file reached
                break
            
        if binary == '':
            raise Exception(f'Invalid jump command - {asm_jump}')


def comp_bin(asm_comp):
    
    """ Goes through the alu_bin file and searchs for the equivalent
        binary instruction of the comp assembly instruction.
    """
    binary = ''
    with open(ALU_bin_file) as alu: #rememeber to put the actual file
        while True:
            instruction = alu.readline()
            if instruction:
                instruction = instruction.strip()
                if instruction.startswith(asm_comp):
                    if 'M' in asm_comp:
                        binary = '1' + instruction.split(' ')[1]
                        return binary
                    else:
                        binary = '0' + instruction.split(' ')[1]
                        return binary
            else:
                break
        if asm_comp == '' and binary == '':
            raise Exception(f'Invalid syntax no comp command passed {asm_comp}')
        else:
            raise Exception(f'Invalid comp command. No such command as {asm_comp}.')
            
    
        
