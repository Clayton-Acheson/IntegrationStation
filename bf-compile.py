#!/usr/bin/python
program=">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
endline=""

outputfile = open("bf-program.bin", "wb")

def compile(i, count):
    opcode = ''
    if i == '>':
        opcode = '000'
    elif i == '<':
        opcode = '001'
    elif i == '+':
        opcode = '010'
    elif i == '-':
        opcode = '011'
    elif i == '.':
        opcode = '100'
    elif i == ',':
        opcode = '101'
    elif i == '[':
        opcode = '110'
    elif i == ']':
        opcode = '111'

    if i == '.' or i == ',':
        binary = f'{opcode}{0:>013b}'
        binary_num = int(binary, 2)
        bytes = binary_num.to_bytes(2, 'little')
        for c in range(count):
            outputfile.write(bytes)
    else:
        binary = f'{opcode}{count:>013b}'
        binary_num = int(binary, 2)
        bytes = binary_num.to_bytes(2, 'little')
        outputfile.write(bytes)

def find_end(start):
    last = program[start]
    start += 1
    jump = 0
    count = 1
    for index, inst in enumerate(program[start:]):
        if last != inst:
            jump += 1
        if inst == '[':
            count += 1
        elif inst == ']':
            count -= 1

        if count == 0:
            return jump + 1
        last = inst
    raise Exception("No matching while end for while start")

def find_start(start):
    last = program[start]
    jump = 0
    count = 1
    for index, inst in reversed(list(enumerate(program[:start]))):
        if last != inst:
            jump += 1
        if inst == ']':
            count += 1
        elif inst == '[':
            count -= 1

        if count == 0:
            return jump
        last = inst
    raise Exception("No matching while start for while end")

last_instruction = program[0]
addup = 0
skip = False
for index, inst in enumerate(program):
    if inst == '[':
        compile(last_instruction, addup)
        addup = 1
        compile(inst, find_end(index))
    elif inst == ']':
        compile(last_instruction, addup)
        addup = 1
        compile(inst, find_start(index))
    else:
        if inst == last_instruction:
            addup += 1;
        else:
            if last_instruction != '[' and last_instruction != ']':
                compile(last_instruction, addup)
            addup = 1
    last_instruction = inst
print("")
outputfile.close()
