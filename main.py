# Initialization #

import argparse, os, sys, time
from builtins import print as printunmodded
filedirectory = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser()
os.system("color")
def print(*args, end='\n', reset_color=True, **kwargs):
    if reset_color: printunmodded(*args, end=f"{end}{FM.reset}", **kwargs)
    else: printunmodded(*args, end=f"{end}", **kwargs)
class FM:
    reset = '\x1b[0m\x1b[49m'
    red, blue, green, yellow, purple, cyan, white, black, \
    light_blue, light_green, light_red, light_purple, light_white, light_black, \
    light_cyan, light_yellow, bold, underline, italic, reverse, strikethrough, \
    remove_color, remove_bold, remove_underline, remove_italic, remove_reverse, \
    remove_strikethrough, bg_red, bg_green, bg_blue, bg_yellow, bg_black, \
    bg_white, bg_light_red, bg_light_green, bg_light_blue, bg_light_yellow, \
    bg_light_black, bg_light_white, bg_purple, bg_light_purple, bg_cyan, bg_light_cyan = (
        '\x1b[31m', '\x1b[34m', '\x1b[32m', '\x1b[33m', '\x1b[35m', '\x1b[36m', '\x1b[37m', '\x1b[30m', '\x1b[94m', '\x1b[92m', '\x1b[91m', '\x1b[95m', '\x1b[97m',
        '\x1b[90m', '\x1b[96m', '\x1b[93m', '\x1b[1m', '\x1b[4m', '\x1b[3m', '\x1b[7m', '\x1b[9m', '\x1b[39m', '\x1b[22m', '\x1b[24m', '\x1b[23m', '\x1b[27m', '\x1b[29m',
        '\x1b[41m', '\x1b[42m', '\x1b[44m', '\x1b[43m', '\x1b[40m', '\x1b[47m', '\x1b[101m', '\x1b[102m', '\x1b[104m', '\x1b[103m', '\x1b[100m', '\x1b[107m', '\x1b[45m',
        '\x1b[105m', '\x1b[46m', '\x1b[106m'
    )
    info, success, error, warning, debug, test = (f'{reverse}{light_blue}[INFO]{remove_reverse}', f'{reverse}{light_green}[SUCCESS]{remove_reverse}', f'{reverse}{light_red}[ERROR]',
    f'{reverse}{light_yellow}[WARNING]{remove_reverse}', f'{reverse}{light_purple}[DEBUG]{remove_reverse}', f'{reverse}{light_cyan}[TEST]{remove_reverse}')\
    
    @staticmethod
    def header_warn(header, msg):
        print(f"{FM.warning} {header}{FM.remove_reverse}\n{msg}")
    @staticmethod
    def header_error(header, msg):
        print(f"{FM.error} {header}{FM.remove_reverse}\n{msg}")
    """    @staticmethod
    def header_info(header, msg):
        print(f"{FM.info} {header}{FM.remove_reverse}\n{msg}")
    @staticmethod
    def header_success(header, msg):
        print(f"{FM.success} {header}\n{msg}")"""
    
# Code Variables/Constants, Classes, Functions, etc. #

regcount = 8 # Default, register count
reg_w_ex = [] # Default, register write exclude (No registers should be excluded by default)
reg_r_ex = [] # Default, register read exclude (No registers should be excluded by default)
start_adr = 0 # Default, start address
mem_size = 512 # Default, memory size
io_in_size = 8 # Default, I/O input size
io_out_size = 8 # Default, I/O output size
comment_no_end = False # For multi-line comments. If set and not unset before file ends, crash.

class Operand():
    def __init__(self, name, bitcount):
        self.name = name
        self.bitcount = bitcount
        self.intlimit = (1 << bitcount) - 1
        self.bitmask = self.intlimit

def main():
    global regcount, reg_w_ex, reg_r_ex, start_adr, mem_size, io_in_size, io_out_size, comment_no_end
    def d1print(*printargs, **kwargs): # Debug print lvl 1, nested function.
        if args.verbose >= 1: print(*printargs, **kwargs)
    def d2print(*printargs, **kwargs): # Debug print lvl 2, nested function.
        if args.verbose >= 2: print(*printargs, **kwargs)
    def d3print(*printargs, **kwargs): # Debug print lvl 3, nested function.
        if args.verbose == 3: print(*printargs, **kwargs)

    d1print(f"{FM.success} Finished initialization, main function started, verbose printing initialized.")
    d2print(f"{FM.info} Attempting to open ISA file.")
    try:
        with open(args.isafile, 'r') as f:
            isa = f.read()
            d1print(f"{FM.success} ISA read.")
            d3print(f"{FM.debug} ISA:\n{isa}")
    except Exception as e:
        FM.header_error("ISA File: Failed to read", f"Exception found while trying to read file.\n\n'{e}'\n\nThe program will now close peacefully.")
        sys.exit(1)
    # We don't need to stay in the 'with' or 'try' block now that we've loaded the file into memory.
    d2print(f"{FM.info} File closed.")
    isalines = isa.splitlines()
    d2print(f"{FM.info} Split ISA into individual lines.")
    d3print(f"{FM.debug} ISA lines:\n{isalines}")
    
    for linenum, line in enumerate(isalines, 0):
        d2print(f"{FM.info} Processing line {linenum} of {len(isalines)}.")
        trim = line.strip() # While most lines are already stripped, some may not.
        
        if trim == "":
            # Empty lines are no use to us.
            d3print(f"{FM.info} Line {linenum} was empty. Continuing.")
            continue
        # We could also do "if line.startswith('#'): continue" here, but it doesn't allow us to handle multi-line comments.
        d3print(f"{FM.debug} Trimmed line: '{trim}'")
        split = trim.split()
        d3print(f"{FM.debug} Split line: '{split}'")

        # Here and now is exactly when we need to start managing comments.
        # If we do not, we're screwed. Badly.

        if "#" in split:
            # Let's find where exactly it's index is..
            ix = split.index("#")
            d3print(f"{FM.debug} Comment found at index {ix}.")
            # Trim everything past it off. It's not a multi-line/start-and-end comment.
            split = split[:ix]
            d3print(f"{FM.info} Found that line contained comment and trimmed everything after comment off.")
        
        # Now, we need to manage start-and-end comments.
        # If we do not, we're screwed. Badly... Once again.
        # Now these ones are the more tricky ones...

        # Now, we could just find the first index that matches #*..
        # After all, the only correct way to do comments in an .isa format is to have a # or #* and then a space.
        # But then, we're screwing ourselves over by being unable to handle ANOTHER start-and-end comment on the same line.
        # But there is an easier way to do this.. We cut out the comments one by one. Then, the first index that matches #* is the next comment.
        
        if not comment_no_end:
            while True: # This is dangerous, but we need to loop until a break because we can technically have infinite comments and need to remove them all.
                if "#*" in split:
                    ix = split.index("#*") # "Returns first index of value"
                    try:
                        ix2 = split.index("*#")
                    except ValueError:
                        # Nope! We're not crashing just yet.
                        # This could mean that it's a multi-line comment. It's end just isn't in our current line!
                        # We need to set a flag instead, and if we do not find that the flag is unset before the file ends, THEN we can crash.
                        comment_no_end = True
                        d2print(f"{FM.warning} Found a comment start, but didn't find a comment ending.")
                        break
                    # Okay, so, we've found a start-and-end comment instead of a multi-line one. Let's remove it.
                    split = split[:ix] + split[ix2+1:]
                    d3print(f"{FM.info} Found start-and-end comment. Removed it.")
                    break
                else:
                    # Nope, it's not. Let's NOT get ourselves into an infinite loop today.
                    break
        else:
            # Oh! We've time travelled now.
            # We tried to remove a start-and-end comment, but found that it was instead multi-line, the harder case to handle.
            # We have to find the ending before we do anything...
            try:
                ix = split.index("*#")
                split = split[:ix]
                d3print(f"{FM.info} Found multi-line comment. Removed it.")
                comment_no_end = False
                # Now, let's reenter this stupid loop to figure out if there's any other comments on this line.
                # If there are, we need to remove them. Maybe this time they'll be start-and-end comments.
                # If not, welp, time to go through this entire thing one more time.
                
                while True: # This is dangerous, but we need to loop until a break because we can technically have infinite comments and need to remove them all.
                    if "#*" in split:
                        ix = split.index("#*") # "Returns first index of value"
                        try:
                            ix2 = split.index("*#")
                            d2print(f"{FM.info} Found the ending to that multi-line comment.")
                        except ValueError:
                            # Nope! We're not crashing just yet.
                            # This could mean that it's a multi-line comment. It's end just isn't in our current line!
                            # We need to set a flag instead, and if we do not find that the flag is unset before the file ends, THEN we can crash.
                            comment_no_end = True
                            d2print(f"{FM.warning} Found a comment start, but didn't find a comment ending.")
                            break
                        # Okay, so, we've found a start-and-end comment instead of a multi-line one. Let's remove it.
                        split = split[:ix] + split[ix2+1:]
                        d3print(f"{FM.info} Found start-and-end comment. Removed it.")
                        break
                    else:
                        # Nope, it's not. Let's NOT get ourselves into an infinite loop today.
                        break
                
            except ValueError:
                # Darn it! It's still not anywhere to be found!
                # Well, in that case, let's ignore this line and check the length of the file...
                if linenum == len(isalines):
                    # Yup, it's the end of the file!
                    # NOW we crash.
                    FM.header_error("ISA File: Invalid configuration", f"Invalid comment (you're missing a valid ending to the comment): No closing valid *# found in the entire file.")
                    sys.exit(1)
                # Okay, so, this isn't the file's end. Cool. Let's just ignore this line.
                continue


        # Okay, so after all of that, we've saved ourselves. Back to normal levels of commenting.

        # I thought I handled these cases, but after the comments are removed, apparently, we did not.
        if len(split) == 0:
            continue # This line is empty, let's go do something else.

        
        if split[0] == "+":
            d1print(f"{FM.info} Found configuration line.")
            
            # Figure out what exactly it's trying to configure
            match split[1]:
                case "REG_COUNT":
                    if len(split) < 4:
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing something): '{trim}', line {linenum}.")
                        sys.exit(1)
                    if split[2] != ":":
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing a valid separator): expected : found '{split[2]}', line {linenum}.")
                        sys.exit(1)
                    try:
                        regcount = int(split[3])
                        if regcount < 1:
                            FM.header_error("ISA File: Invalid configuration", f"Invalid register count '{split[3]}', line {linenum}. Must be an unsigned integer.")
                            sys.exit(1)
                        d1print(f"{FM.info} Configured register count to {regcount}.")
                    except:
                        FM.header_error("ISA File: Invalid configuration", f"Invalid register count '{split[2]}', line {linenum}. Must be an unsigned integer.")
                        sys.exit(1)
                
                case "REG_EXCLUDE_WRITE":
                    if len(split) < 4:
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing something): '{trim}', line {linenum}.")
                        sys.exit(1)
                    if split[2] != ":":
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing a valid separator): expected : found '{split[2]}', line {linenum}.")
                        sys.exit(1)
                    if split[3] != "NUL": 
                        reg_exclude_write = split[3:] # Everything after argument 3
                        d1print(f"{FM.info} Configured register exclude write to {reg_exclude_write}.")
                    else:
                        d1print(f"{FM.info} Configuration was set to nothing. No changes.")
                    
                
                case "REG_EXCLUDE_READ":
                    if len(split) < 4:
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing something): '{trim}', line {linenum}.")
                        sys.exit(1)
                    if split[2] != ":":
                        FM.header_error("ISA File: Invalid configuration", f"Invalid configuration (You're missing a valid separator): expected : found '{split[2]}', line {linenum}.")
                        sys.exit(1)
                    if split[3] != "NUL": 
                        reg_exclude_read = split[3:] # Everything after argument 3
                        d1print(f"{FM.info} Configured register exclude read to {reg_exclude_read}.")
                    else:
                        d1print(f"{FM.info} Configuration was set to nothing. No changes.")
                
                case _:
                    d1print(f"{FM.warning} Config line not recognized.")
        
# Run #
if __name__ == "__main__": # In *no case* should this be an import.
    # Arguments #
    parser.add_argument("isafile", type=str, help="The input .isa file(path). This file will be used as the microcode/ISA for the universal assembler.")
    parser.add_argument("asmfile", type=str, help="The input assembly file(path), which must match the ISA within the specified .isa file.")
    parser.add_argument("-b", "--bin", action="store_true", help="Binary output, no matter the output method (file, stdout). This is set by default.")
    parser.add_argument("-x", "--hex", action="store_true", help="Hexadecimal output, no matter the output method (file, stdout).")
    parser.add_argument("-o", "--out", type=str, help="Output file(path). If not set, output will be printed to stdout.")
    parser.add_argument("-d", "-v", "--verbose", type=int, help="Prints debug info/verbose mode. Level 1 is the lowest logging level, with level 3 being the highest logging level.")
    parser.add_argument("-c", "--combined", action="store_true", help="If set, any whitespace will be removed from the output, regardless of the output method.")

    # Argument Handling, Program Running #
    
    args = parser.parse_args()
    
    # Subsection: Argument Errors
    if args.verbose is not None:
        if args.verbose > 3 or args.verbose < 0: raise ValueError("Invalid logging level. Use 0 for none, 1 for low, 2 for medium, or 3 for highest.")
    if args.verbose is None: args.verbose = 0
    
    #print(args) # Debug
    
    # Subsection: Running #
    main()

else:
    raise ImportError("This is **not** a module. It is an executable Python script. Please remove any line importing this and use uniasm3 itself.")
