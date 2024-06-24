import sys

class InvalidStructure(Exception): ...



def func_caller(instructions: list[str], funcs:dict[str, list[str]], stack: list[int]):
    layer = 0

    if_pos: list[int] = [-1] * len(instructions)
    else_pos: list[int] = [-1] * len(instructions)
    then_pos:list[int] = [-1] * len(instructions)
    for index, i in enumerate(instructions):
        if i == 'if':
            if_pos[layer] = index
            layer += 1
        if i == 'else':
            else_pos[layer] = index
        if i == 'then':
            then_pos[layer] = index
            layer -= 1
    if_pos = [v for v in if_pos if v != -1]
    else_pos = [v for v in else_pos if v != -1]
    then_pos = [v for v in then_pos if v != -1]
    if not (len(if_pos) == len(else_pos) == len(then_pos)):
        raise InvalidStructure
    fast_forward = -1
    statement_value = {}
    for index, i in enumerate(instructions):
        if index < fast_forward:
            continue
        if not i:
            continue
        if i == 'if':
            v = stack.pop()
            statement_value[index] = bool(v)
            statement_value[else_pos[if_pos.index(index)]] = not bool(v)
            if not statement_value[index]:
                fast_forward = else_pos[if_pos.index(index)]
            continue
        if i == 'else':
            if not statement_value[index]:
                fast_forward = then_pos[else_pos.index(index)]
            continue
        if i == 'then':
            continue
        if i.startswith('."') and i.endswith('"'):
            sys.stdout.write(i[2:-1])
            continue
        try:
            if int(i):
                stack.append(int(i))
                continue
        except:
            pass
        match i:
            case '.':
                v = stack.pop(-1)
                sys.stdout.write(str(v) + ' ')
            case '+':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(v1 + v2)
            case '-':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(v1 - v2)
            case '*':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(v1 * v2)
            case '/':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(v1 // v2)
            case 'dup':
                stack.append(stack[-1])
            case 'swap':
                stack[-2], stack[-1] = stack[-1], stack[-2]
            case 'mod':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(v1 % v2)
            case 'depth':
                stack.append(len(stack))
            case 'clearstack':
                for _ in range(len(stack)):
                    stack.pop(-1)
            case '=':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(-(v1 == v2))
            case '>':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(-(v1 > v2))
            case '<':
                v2 = stack.pop(-1)
                v1 = stack.pop(-1)
                stack.append(-(v1 < v2))
            case _:
                if i in funcs:
                    func_caller(funcs[i], funcs, stack)
                    continue
                else:
                    raise InvalidStructure


def caller(instructions: list[str], funcs:dict[str, list[str]], stack: list[int]):
    quote_mode: bool = False
    quote = ""
    func_mode: bool = False
    func_name = None
    func_instructions = []
    for i in instructions:
        if quote_mode:
            if '"' in i:
                splited = i.split('"', maxsplit=1)
                quote += splited[0]
                if not func_mode:
                    sys.stdout.write(quote)
                else:
                    func_instructions.append(f'." {quote}"')
                quote_mode = False
                if len(splited)==2:
                    i = i.split('"', maxsplit=1)[1]
                else:
                    continue
            else:
                quote += f'{i} '
                continue
        if i == '."' and not quote_mode:
            quote_mode = True
            quote = ""
            continue
        if not quote_mode:
            if i == ';' and func_mode:
                func_mode = False
                funcs[func_name] = func_instructions
                func_name = ''
                func_instructions = []
                continue
            if func_mode and not func_name:
                func_name = i
                continue
            if func_mode and func_name:
                func_instructions.append(i)
                continue
            if i == ':' and not func_mode:
                func_mode = True
                continue
            try:
                if int(i):
                    stack.append(int(i))
                    continue
            except:
                pass
            match i:
                case '.':
                    v = stack.pop(-1)
                    sys.stdout.write(str(v) + ' ')
                case '+':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(v1+v2)
                case '-':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(v1 - v2)
                case '*':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(v1 * v2)
                case '/':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(v1 // v2)
                case 'dup':
                    stack.append(stack[-1])
                case 'swap':
                    stack[-2], stack[-1] = stack[-1], stack[-2]
                case 'mod':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(v1 % v2)
                case 'depth':
                    stack.append(len(stack))
                case 'clearstack':
                    for _ in range(len(stack)):
                        stack.pop(-1)
                case '=':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(-(v1 == v2))
                case '>':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(-(v1 > v2))
                case '<':
                    v2 = stack.pop(-1)
                    v1 = stack.pop(-1)
                    stack.append(-(v1 < v2))
                case _:
                    if i in funcs:
                        func_caller(funcs[i], funcs, stack)
                        continue
                    else:
                        raise InvalidStructure



def repl():
    funcs: dict[str, list[str]] = {}
    stack: list[int] = []
    while True:
        sys.stdout.write('>> ')
        sys.stdout.flush()
        instruction = sys.stdin.readline().strip('\n ')
        try:
            caller(instruction.split(' '), funcs, stack)
            sys.stdout.write(f' ok {len(stack)}')
        except Exception as e:
            sys.stdout.write(' ' + repr(e.__class__))
        sys.stdout.write('\n')
        sys.stdout.flush()

repl()