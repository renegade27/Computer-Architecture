"""CPU functionality."""

import sys

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        #Commands binded with opcodes
        self.commands = {
            0b00000001: self.hl t,
            0b10000010: self.ldi,
            0b01000111: self.prn,
        }
        pass
    
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

    def load(self):
        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
                sys.exit() 
        pass
