"""CPU functionality."""

import sys

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 244
        self.pc = self.reg[0]
        #Commands binded with opcodes
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b10100000: self.add,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b10100111: self.cmp
        }
        self.E = 0  # 0 == false, 1 == true
        self.L = 0 # 1 == regA.value < regB.value
        self.G = 0 # 1 == regA.value > regB.value

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    #Stop program
    def hlt(self, operand_a, operand_b):
        return (0, False)

    #Sets a specified register to a certain value
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        #Since we're evaluating 2 items in reg, advance 3 spaces
        return (3, True)

    #Prints a specified value in register
    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        #Since we're evaluating only 1 item in reg, advance 2 spaces
        return (2, True)
    
    def add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        return (3, True)

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def push(self, operand_a, operand_b):
        reg_address = self.ram[self.pc + 1]
        self.sp -= 1
        value = self.reg[reg_address]
        self.ram[self.sp] = value
        return (2, True)

    def pop(self, operand_a, operand_b):
        pop_value = self.ram[self.sp]
        # reg_address = self.ram[self.pc + 1]
        self.reg[operand_a] = pop_value
        self.sp += 1
        return (2, True)

    # Jump to address in given register (program counter + 1 of ram)
    def jmp(self, operand_a, operand_b):
        jump_address = self.reg[operand_a]
        self.pc = jump_address
        return(0, True)

    # Compare our next 2 registers where position = operands and set our flags
    def cmp(self, operand_a, operand_b):

        # RESET Flags for subsequent compares ?
        self.E = 0
        self.L = 0
        self.G = 0

        value_one = self.reg[operand_a]
        value_two = self.reg[operand_b]

        if value_one == value_two:
            self.E = 1
        elif value_one < value_two:
            self.L = 1
        elif value_one > value_two:
            self.G = 1
        
        return(3, True)

    # If our E flag is clear, jump to given register at operand_a. Else, continue into our program
    def jne(self, operand_a, operand_b):
        if self.E == 0:
            self.pc = self.reg[operand_a]
            return(0, True)
        else:
            return(2, True)

    # If our E flag is set, jump to given register at operand_a. Else, continue into our program
    def jeq(self, operand_a, operand_b):
        if self.E == 1:
            self.pc = self.reg[operand_a]
            return(0, True)
        else:
            return(2, True)

    def load(self, program):
        address = 0

        # For now, we've just hardcoded a program:

        with open(program) as f:
            program = []

            for line in f:
                comment_split = line.split('#')
                number = comment_split[0].strip()
                try:
                    program.append(int(number, 2))
                except ValueError:
                    pass
        
        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        # multiplication
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        #While our program is running
        while running:
            # Our instruction register
            ir = self.ram[self.pc]

            # Set our operands
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                #Based on OP code, we pass our operands into one of our
                #functions accessing through our commands key:value
                operation_output = self.commands[ir](operand_a, operand_b)
                #We return True unless HLT then false, this is the 2nd value
                #In the tuple that is returned
                running = operation_output[1]
                #We increase our PC so we can move forward in our RAM
                self.pc += operation_output[0]

            except:
                #If OP Code is unknown, this will fire
                print(f"Unknown command: {ir}")
                print(self.reg)
                sys.exit() 
