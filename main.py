#8-BIT CPU emulator created in python using the SCASM instruction set.
#100 bytes of RAM
#PROGRAM INSTRUCTIONS:
#  REG [REG] 
#  ADD [REG] [REG] (Or you can add a raw number)
#  SUB [REG] [REG] (Again, you can use a raw number)
#  STORE [REG] [RAM ADDRESS 0 to 100]
#  JUMP [LINE NUMBER]
#  MOV [REG] [REG]
#  IN [REG]
#  RAM
#  HALT
#CPU COMMANDS:
#  RUN
#  REGS
#  RAM
#  EXIT
#  LOAD [FILE NAME]
#
#To run a program you need to make the file first in an editor.

#Define registers
regs = {
'A': 0, 
'B': 0, 
'C': 0, 
'D': 0, 
'E': 0, 
'F': 0, 
'G': 0, 
'H': 0,
}

#Define RAM size
ram = [0] * 1024
pc = 0

#Function for the RUN command
def run():
    global pc, Z
    pc = 0
    Z = 0
    while pc < len(program):
        instr = program[pc]
        op = instr[0]

        if op == "REG":
            # instr = ('REG', 'A', 10)
            if len(instr) != 3:
                print(f"Error: REG instruction requires 2 parameters at line {pc}")
                break
            _, r, val = instr
            regs[r] = val

        elif op == "LOAD":
            # instr = ('LOAD', 'A', 10)
            if len(instr) != 3:
                print(f"Error: LOAD instruction requires 2 parameters at line {pc}")
                break
            _, r, addr = instr
            regs[r] = ram[addr]

        elif op in ("ADD", "SUB", "STORE", "MOV", "IN"):
            if len(instr) != 3:
                print(f"Error: {op} instruction requires 2 parameters at line {pc}")
                break
            r1 = instr[1]
            r2_or_val = instr[2]
            if op == "ADD":
                if isinstance(r2_or_val, int):
                    regs[r1] = (regs[r1] + r2_or_val) & 0xFF
                else:
                    regs[r1] = (regs[r1] + regs[r2_or_val]) & 0xFF
            elif op == "SUB":
                if isinstance(r2_or_val, int):
                    regs[r1] = (regs[r1] - r2_or_val) & 0xFF
                else:
                    regs[r1] = (regs[r1] - regs[r2_or_val]) & 0xFF
            elif op == "STORE":
                addr = r2_or_val
                ram[addr] = regs[r1]
            elif op == "MOV":
                r2 = r2_or_val
                if r2 in regs:
                    regs[r1] = regs[r2]
                else:
                    regs[r1] = int(r2)
            elif op == "IN":
                val = int(input("> "))
                regs[r1] = val & 0xFF

        elif op == "JUMP":
            if len(instr) != 2:
                print(f"Error: JUMP requires 1 parameter at line {pc}")
                break
            _, addr = instr
            pc = addr
            continue

        elif op == "RAM":
            print(ram)

        elif op == "CMP":
            r1 = instr[1]
            r2 = instr[2]
            if regs[r1] == regs[r2]:
                Z = 1
            else:
                Z = 0
            pc += 1
            continue

        elif op == "JZ":
            if len(instr) != 2:
                print(f"Error: JZ requires 1 parameter at line {pc}")
                break
            _, line_number = instr
            if Z == 1:
                pc = line_number
                continue
            else:
                pc += 1
                continue

        elif op == "HALT":
            break

        else:
            print(f"Unknown instruction {op} at line {pc}")

        pc += 1
             
#Function to load file
def load_file(filename):
    global program
    prog = []
    with open(filename) as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith(";"):
                continue
            parts = line.split()
            print(f"Line {line_number}: '{line}', parts: {parts}")  # Debug print
            
            op = parts[0].upper()
            
            if op == "LOAD":
                # LOAD REG ADDRESS
                try:
                    r = parts[1].upper()
                    addr = int(parts[2])
                    prog.append((op, r, addr))
                except Exception as e:
                    print(f"Error parsing LOAD at line {line_number}: {e}")
            
            elif op in ("ADD", "SUB", "STORE", "MOV", "IN"):
                # These expect: OP R V or R R
                r = parts[1].upper()
                try:
                    v = int(parts[2])
                    prog.append((op, r, v))
                except:
                    # If not a number, treat as register
                    prog.append((op, r, parts[2].upper()))
            
            elif op == "JUMP":
                # JUMP LINE_NUMBER
                try:
                    line_num = int(parts[1])
                    prog.append((op, line_num))
                except:
                    print(f"Invalid JUMP line {line_number}")
            
            elif op == "HALT":
                prog.append((op,))
            
            elif op == "REG":
                # REG R V
                if len(parts) == 3:
                    try:
                        r = parts[1].upper()
                        val = int(parts[2])
                        prog.append((op, r, val))
                    except:
                        print(f"Invalid REG instruction at line {line_number}")
                else:
                    print(f"Invalid REG instruction at line {line_number}")
            
            # Handle CMP instruction
            elif op == "CMP":
                # CMP R R
                if len(parts) != 3:
                    print(f"Invalid CMP instruction at line {line_number}")
                    continue
                r1 = parts[1].upper()
                r2 = parts[2].upper()
                prog.append((op, r1, r2))
            
            # Handle JZ instruction
            elif op == "JZ":
                # JZ line_number
                if len(parts) != 2:
                    print(f"Invalid JZ instruction at line {line_number}")
                    continue
                try:
                    line_num = int(parts[1])
                    prog.append((op, line_num))
                except:
                    print(f"Invalid line number for JZ at line {line_number}")
            
            else:
                print(f"Unknown instruction '{line}' at line {line_number}")
    program = prog
    print(f"Loaded {len(program)} instructions from {filename}")
    return prog
#Command loop
while True:
    cmd = input("CPU:").strip().upper().split()
    if not cmd:
        continue
    if cmd[0] == "RUN":
        run()
        print("regs=", regs, "ram[0:4]=", ram[0:4])
    elif cmd[0] == "REGS":
        print(regs)
    elif cmd[0] == "RAM":
        print(ram)
    elif cmd[0] == "REG" and len(cmd) == 3:
        regs[cmd[1]] = int(cmd[2])
    elif cmd[0] == "EXIT":
        break
    elif cmd[0] == "LOAD" and len(cmd):
        load_file(cmd[1])
    else:
        print("cmds: RUN, REGS, RAM, REG A 20, LOAD, EXIT")
        

