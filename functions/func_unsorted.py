




"""

def get_all_lines_from_pgn(pgnpath):
    print(f"Importing pgn from {pgnpath}")
    with open(pgnpath) as f:
        fullpgn = f.readlines()
    pgn = []
    for line in fullpgn:
        if line != '\n' and line[0] != '[':
            pgn.append(line)
    all_lines = []
    for long_line in pgn:
        for i in range(long_line.count('{')):
            for j in range(len(long_line)):
                if long_line[j] == '{':
                    indexparopen = j
                elif long_line[j] == '}':
                    long_line = long_line[:indexparopen]+long_line[j+1:]
                    break
        while long_line != '':
            last_oppening_parenthesis = 0
            last_closing_parenthesis = 0
            prems = True
            for i,char in enumerate(long_line):
                if char == '*' and prems:
                    all_lines.append(clean_line(long_line[:-3]))
                    long_line = ''
                if char == '(':
                    last_oppening_parenthesis = i
                if char == ')' and prems:
                    prems = False
                    last_closing_parenthesis = i
                    raw_line = long_line[:i]
                    all_lines.append(clean_line(raw_line))
                    if last_closing_parenthesis != len(long_line)-1:
                        long_line = long_line[0:last_oppening_parenthesis]+long_line[last_closing_parenthesis+1:]
                    else:
                        long_line = long_line[0:last_oppening_parenthesis]
                    last_oppening_parenthesis = 0
                    last_closing_parenthesis = 0
    return(all_lines)

"""

