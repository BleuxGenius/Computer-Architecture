"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # step one add constructor (memory)
        self.ram = [0] * 256
        # register( general purpose registers)
        self.registers = [0] * 8
        # reset the stack pointer 
        self.registers[7] = 0xF4 

    #    store program counter 
        self.pc = self.registers[0]
        # store the flags 
        self.fl = self.registers[4]
        # store the stack pointer 
        self.SP = self.registers[7]
        self.SP = 244
        self.running = True

        # store operation handling/ branch table
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000110: self.pop,
            0b01000101: self.push
        }
        
    def __repr__(self):
        return f"RAM: {self.ram} Register: {self.ram}"

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):
        # halts cpu 
        return (0, False)

    def ldi(self, operand_a, operand_b):
        # sets register to value
        self.registers[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        # print value at register
        print(self.registers[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        # multiply two values to store in register
        self.alu(MUL, operand_a, operand_b)
        return (3, True)

    def pop(self, operand_a, operand_b):
        # gets value from memory at stack pointer
        value = self.ram_read(self.SP)
        # write that value to indicated spot in register
        self.registers[operand_a] = value
        # increment stack pointer to next filled spot in stack memory
        self.SP += 1
        return (2, True)

    def push(self, operand_a, operand_b):
        # decrements SP to next open spot in stack memory
        self.SP -= 1
        # grabs value from indicated register spot
        value = self.registers[operand_a]
        # writes value to RAM at stack pointer address
        self.ram_write(value, self.SP)
        return (2, True)

    def load(self, program_filepath):
        """Load a program into memory."""
        try:

            address = 0
    # Open program file, loop -> parse line (ignore comments), store into memory at address, inc address
        # program_file = open(input_file, "r")
        # for line in program_file
            # Remove whitespace
            # Ignore blank lines
            # Ignore lines that start with comments
            # All instructions are 1 byte so just
            # take the first 8 chars and convert
            # to a binary number
            # Insert instruction into memory
            # Inc to next pos in memory
            with open(self.program_filepath) as f:
                for line in f:
                    line = line.split("#")[0]
                    line = line.strip()
                    if line == '':
                        continue
                # line = int(line) # For the daily project we want int(line, 2) <- saying we want base 2 for binary
                self.ram[address] = int(line, 2)
                address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1] not found}")        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = self.ram[self.pc]
         
        if len(sys.argv) != 2:
            print("usage: cpu.py filename")
            sys.exit(1)

            # get program file 
        self.program_filepath = sys.argv[1]
            # load program into memory 
        self.load()    

        while running:
            # use program counter to get current instruction 
                IR = self.ram[self.pc]
                # oprands for the instruction 
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                try:
                    operation_output = self.commands[IR](operand_a, operand_b)
                    running = operation_output[1]
                    self.pc += operation_output[0]
                except:
                        print("Unknown command: {IR}")
                        sys.exit(1)

cpu = CPU()
cpu.run()