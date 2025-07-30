""" This is the parser module, it is part of the assembler package for the hack assmebly program.
    It takes in an input file of the form "file.asm" which contains the assembly program for the
    hack computer, and parses it into a suitable format for the assembler to process."""

import os, re


#Unrelated;
""" Assembler gets a file path, checks if its an abs path. Else checks if its in current directory,
    else search for it in the provided directory by user."""

#The constructor

def make_parser(filePath:str):
    """
        Opens the input .asm file and gets ready to parse it.

        Args:
            file_path: The path to the .asm file."""
    if not os.path.exists(filePath):
        raise FilenotFoundError(f'file not found: {filePath}')
    
    file = open(filePath, mode='r')

    #__HELPER FUNC__
    def cleanLine(text_line):
        #strip whitespaces at the beginning and end of line
        text = text_line.strip()
        
        if text:    #text isn't empty
            if text.startswith('//'): #check if text is a comment
                return ""
            else: #text is an actual command
                """ add mechanism to remove whitespaces within the command. we can use the 're' regular
                    expression module for a more efficient matching where there are more than 1 white
                    space within the text 
                """
                newtext = ''.join(text.split(' ')) #remove whitespace within command
                #if there's is a comment along the line of the command we remove it bfr passing the command
                if '//' in newtext:
                    newtext = newtext.split('//')[0]
                    return newtext.strip('\n\t ')
                else:
                    return newtext
        else: #text is an empty string
            return text
    

    def get_nextValidCommand() -> str or None:
        """This returns a string of a valid hack command, skips comments and whitespace lines"""
        nonlocal file
        while True:
            line = file.readline()
            if line: #line isn't empty hence not EOF
                cleaned_line = cleanLine(line)
                if cleaned_line:
                    return cleaned_line
               
            else: #line is empty hence EOF
                return None


    """__STATE VARIABLES__"""            
    #initialize the current line and next line, the current line is initially set to ''
    current_command = ''
    next_command = get_nextValidCommand()
        


    def hasMoreLines():
        nonlocal next_command
        if next_command != None or next_command != '':
            return True
        else:
            return False

    def advance():
        """ This sets the current command to the next available command if there are any"""
        nonlocal current_command, next_command
        if hasMoreLines():
            current_command = next_command
            next_command = get_nextValidCommand()

    def instructionType():
        nonlocal current_command
        
        if current_command is None:
            raise ValueError("No current command. Call advance() first.")
        
        if current_command.startswith('@'):
            return "A_INSTRUCTION"
        elif current_command.startswith('(') and current_command.endswith(')'):
            return "L_INSTRUCTION"
        else:
            return 'C_INSTRUCTION'

    def symbol():
        """ Returns the symbolic or numerical part (i.e xxx in @xxx) of the A-instruction
        """
        nonlocal current_command
        if current_command.startswith('@'):
            return current_command.split('@')[1]
        elif current_command.startswith('(') and current_command.endswith(')'):
            return current_command.strip('()')
        else:
            return ''


    def dest() -> str:
        """ Returns the dest part of the current C-instruction
        """
        #we first check if the dest part is inside the C-instruction.
        #For there to be a dest part, an '=' must be in the instruction
        nonlocal current_command
        if '=' in current_command:
            return current_command.split('=')[0]
        else:
            return ''


    def comp() -> str:
        """ Returns the corresponding comp part of the C-instruction returns None/empty sting
            other wise or we can signal the code generating module to raise an error if there's
            no comp part. Comp part is mandatory.
        """
        nonlocal current_command
        text = current_command
        comp = ''
        
        if '=' not in text and ';' not in text:
            return comp #returns an empty str that indicates invalid instruction was passed 
        #if there's a dest part in the instruction we remove it
        if '=' in text:
            text = current_command.split('=')[1]
        #if there's a jump part in the instruction we remove it
        if ';' in text:
            text = text.split(';')[0]
            
        comp = text
        return comp #can be an empty string 


    def jump() ->str:
        """ Returns the jump part of the current C-instruction
        """
        nonlocal current_command
        jump = current_command
        if '=' in current_command:
            jump = current_command.split('=')[1]
        if ';' in jump:
            jump = jump.split(';')[1]
            return jump

        return ''

    def close_file():
        nonlocal file
        try:
            file.close()
            return 'OK'
        except Exception as e:
            return f'Error {e} caused file not to close'

    def getCurrentInstr():
        return current_command


    def message(m):
        if m == 'hasMoreLines':
            return hasMoreLines()
        
        elif m == 'advance':
            return advance()

        elif m == 'instructionType':
            return instructionType()
        
        elif m == 'symbol':
            return symbol()
        
        elif m == 'dest':
            return dest()
        
        elif m == 'comp':
            return comp()
        
        elif m == 'jump':
            return jump()
        elif m == 'close_file':
            return close_file()
        #tester
        elif m == "getCurrentInstr":
            return getCurrentInstr()
        else:
            #raise Exception(m, 'Invalid command - no such command {m}')
            raise Exception(f'Invalid command - no such command {m}')

    return message


def has_more_lines(parser):
    return parser('hasMoreLines')

def advance (parser):
    return parser('advance')

def instructionType(parser):
    return parser('instructionType')

def symbol(parser):
    return parser('symbol')

def dest(parser):
    return parser('dest')

def comp(parser):
    return parser('comp')

def jump(parser):
    return parser('jump')

def close_file(parser):
    return parser('close_file')

def getCurrentCommand(parser):
    return parser('getCurrentInstr')






        

    


        
        
