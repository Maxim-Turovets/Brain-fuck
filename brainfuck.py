import sys


def Interpret(code, raise_on_invalid=True, raise_on_exceeded_bounds=True):
    code     = list(code)
    memory   = [0 for x in range(0, 30000)]
    loops    = []
    output   = ''
    pointer  = 0
    register = 0
    ignore   = False

    while pointer < len(code):
        opcode = code[pointer]

        if ignore:
            if opcode == ']':
                ignore = False

        elif opcode not in ['<', '>', '[', ']', '+', '-', '.']:
            if raise_on_invalid:
                raise Exception('Unknown opcode "%s" at location %i' % (opcode, pointer))

        else:
            if opcode == '>':
                register += 1

                if register >= len(memory):
                    raise Exception('Buffer overflow at location %i' % pointer)

            elif opcode == '<':
                register -= 1

                if register < 0:
                    raise Exception('Buffer underflow at location %i' % pointer)

            elif opcode == '+':
                memory[register] += 1

                if memory[register] > 255:
                    if raise_on_exceeded_bounds:
                        raise Exception('Memory overflow at location %i' % pointer)

                    else:
                        memory[register] = 0

            elif opcode == '-':
                memory[register] -= 1

                if memory[register] < 0:
                    if raise_on_exceeded_bounds:
                        raise Exception('Memory underflow at location %i' % pointer)

                    else:
                        memory[register] = 255

            elif opcode == '.':
                output += chr(memory[register])

            elif opcode == '[':
                if memory[register] == 0:
                    ignore = True

                else:
                    loops.append(pointer)

            elif opcode == ']':
                if len(loops) == 0:
                    raise Exception('Loop end when no loops open at location %i' % pointer)

                pointer = loops.pop() - 1
            
        pointer += 1
        continue

    return output

code = '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+++++++++++++++++++++++++++++.+++++++..+++.-------------------------------------------------------------------------------.+++++++++++++++++++++++++++++++++++++++++++++++++++++++.++++++++++++++++++++++++.+++.------.--------.-------------------------------------------------------------------.-----------------------.'
try:
    result = Interpret(code, True)
    print('Output: %s' % result)

except Exception:
    print('Failed to interpret code: %s' % sys.exc_info()[1])