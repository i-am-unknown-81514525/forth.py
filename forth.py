import sys

class InvalidStructure(Exception): ...


def func_caller(instructions: list[str], funcs:dict[str, list[str]], stack: list[int]):
    run_state = True
    layer = 0
    skip = False
    for i in instructions:
        if not i:
            continue
        if i == 'if':
            if skip:
                layer += 1
                continue
            run_state = stack.pop()
            if not run_state:
                skip = True
            continue
        if i == 'else':
            if run_state:
                if skip:
                    layer += 1
                    continue
                skip = True
            if not layer and not run_state:
                skip = False
            continue
        if i == 'then':
            if layer:
                layer -= 1
            continue
        if layer or skip:
            continue
        if i.startswith('."') and i.endswith('"'):
            sys.stdout.write(i[2:-1])
            continue
        if i.isdigit():
            stack.append(int(i))
            continue
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
            if i.isdigit():
                stack.append(int(i))
                continue
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