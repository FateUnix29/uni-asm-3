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
    f'{reverse}{light_red}[WARNING]', f'{reverse}{light_purple}[DEBUG]{remove_reverse}', f'{reverse}{light_cyan}[TEST]{remove_reverse}')\
    
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

print(f"{FM.success} Finished initialization.")




# Run #
if __name__ == "__main__": # In *no case* should this be an import.
    # Arguments #
    parser.add_argument("isafile", type=str, help="The input .isa file(path). This file will be used as the microcode/ISA for the universal assembler.")
    parser.add_argument("asmfile", type=str, help="The input assembly file(path), which must match the ISA within the specified .isa file.")
    parser.add_argument("-b", "--bin", action="store_true", help="Binary output, no matter the output method (file, stdout). This is set by default.")
    parser.add_argument("-x", "--hex", action="store_true", help="Hexadecimal output, no matter the output method (file, stdout).")
    parser.add_argument("-o", "--output", type=str, help="Output file(path). If not set, output will be printed to stdout.")
    parser.add_argument("-d", "-v", "--debug", action="store_true", help="Prints debug info/verbose mode.")
    parser.add_argument("-c", "--combined", action="store_true", help="If set, any whitespace will be removed from the output, regardless of the output method.")

    # Argument Handling, Program Running #
    args = parser.parse_args()
    with open(args.file, "r") as f:
        print(f.read())
else:
    raise ImportError("This is **not** a module. It is an executable Python script. Please remove any line importing this and use uniasm3 itself.")
