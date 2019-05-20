from nlp import *
from nltk.corpus import wordnet

table = {"procedure":"func","end":"func", "≤":"<=", "function":"func", "--":"#","#":"#","//":"#", "var":"", "let":"func","switch":"func","make":"func","None":"None", "NULL":"None","for":"func","else":"func" ,"or":"or", "let":"func", "show":"func", "equals":"=","\leq":"<=","\geq":">=","while":"func",":=":"=", "<-":"=", "swap": "func", "and":"and", "\n":"\n", "algorithm":"func", "forever":"True", "loop":"func", "then":"", "if":"func", "set":"func", "initialize":"func", "do":"", "input":"func", "add":"func", "print":"func", "in":"in"}

numbers = {"zero": "0", "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9", "ten":"10", "eleven":"11", "twelve":"12", "thirteen":"13", "fourteen":"14", "fifteen":"15", "sixteen":"16", "seventeen":"17", "eighteen":"18", "nineteen":"19", "twenty":"20"}

functions = {"procedure":"DEFINITION", "end":"REMOVELINE","function":"DEFINITION","swap":"SWAP", "switch":"SWAP", "make":"EQUALITY","for":"CONDITIONAL","else":"CONDITIONAL", "let":"EQUALITY","show":"DISPLAY", "while":"CONDITIONAL", "algorithm":"FUNCTION", "loop":"LOOP", "set":"EQUALITY" , "initialize":"EQUALITY", "add":"ADD", "input":"INPUT", "print":"DISPLAY", "if":"CONDITIONAL" }

userdefined_variables = {}
userdefined_functions = {}

equality_delimeters = ["to", "as", "be", "with"]
definition_delimeters = ["to", "as", "be", "with"]


def combine_tables(table1, table2):
    z = table1.copy()
    z.update(table2)
    return z

def init():
    global table
    global equality_delimeters
    global definition_delimeters

    newtable = {}
    for item in table:
        synonyms = syn_ant(item)
        cnt = 0
        for s in synonyms:
            if cnt > 10: break
            if s not in table:
                if table[item] == "func":
                    newtable[s] = "func"
                    functions[s] = functions[item]
                else:
                    newtable[s] = table[item]
            cnt += 1

    table = combine_tables(table, newtable)
    table = combine_tables(table, numbers)
    print(table)
    print(functions)
    new_equality_delimeters = []
    for d in equality_delimeters:
        for s in syn_ant(d):
            new_equality_delimeters.append(s)

    equality_delimeters = new_equality_delimeters

    new_definition_delimeters = []
    for d in definition_delimeters:
        for s in syn_ant(d):
            new_definition_delimeters.append(s)

    definition_delimeters = new_definition_delimeters

def syn_ant(word):
    # print("16")
    synonyms = []
    for syn in wordnet.synsets(word):
        # antonyms = []
        cnt = 0
        for l in syn.lemmas():
            synonyms.append(l.name())
            if cnt > 10: break
            cnt += 1
            # if l.antonyms():
            #     antonyms.append(l.antonyms()[0].name())
        # print("syn_ant", synonyms, antonyms)

    return synonyms

def createFunctionString(line, ind):
    # print("10", line, ind, line[ind])
    # print("11", functions[line[ind]])

    argname = functions[line[ind]]
    invalid_args_following_func = 0
    for i in range(ind+1, len(line)):
        # print(line[i])
        if line[i] in table:
            break
        invalid_args_following_func += 1
    # print("line is ", line)
    # # print("invalid arguments following function:", invalid_args_following_func)
    # if num_args == "FORCONDITIONAL":
    #
    #     arg1 = "".join()
    if argname == "REMOVELINE":
        return "", len(line), False
    if argname == "CONDITIONAL":

        arg1 = "".join(line[ind+1:ind+1+invalid_args_following_func])
        # print("56", arg1)
        line.append(":")

        return line[ind] + " " + arg1 + " ", ind+invalid_args_following_func+1, True
    if argname == "DEFINITION":

        if line[-1] in definition_delimeters:
            del line[-1]

        line.append(":")
        line[ind] = "def"
        return "def", ind+1, False
    
    if argname == "LOOP":
        line.append(":")
        return "while", ind+1, True
    if argname == "DISPLAY":
        retval = ""
        ind += 1
        temp_arg1 = "".join(line[ind:])
        if temp_arg1 in userdefined_variables or temp_arg1 in userdefined_functions:
            retval = "print("
            retval += temp_arg1
            retval += ")"
        else:
            retval = "print(\" "
            while ind < len(line):
                retval += line[ind] + " "
                ind += 1
            retval += " \")"
        return retval, ind + 1, False

    if argname == "EQUALITY":
        ind += 1
        argline = line[ind:]
        # print("91", argline)

        for item in equality_delimeters:
            if item in line:
                keyword = item
                break

        to_ind = line.index(keyword)
        arg1 = arg2 = ""
        if to_ind != -1:
            arg1 = "".join(line[ind:to_ind])
            arg2 = "".join(line[to_ind+1:])

        else:
            if invalid_args_following_func % 2 ==0:
                for i in range(ind + invalid_args_following_func // 2):
                    arg1 += line[i]

                for i in range(ind + (invalid_args_following_func) // 2, ind + invalid_args_following_func):
                    arg2 += line[i]
            else:
                for i in range(ind + (invalid_args_following_func - 1) // 2):
                    arg1 += line[i]

                for i in range(ind + (invalid_args_following_func - 1) // 2, ind + invalid_args_following_func):
                    arg2 += line[i]

        # ind += 1
        # arg1 = line[ind]
        # ind += 2
        # arg2 = line[ind]
        if arg2 in numbers:
            userdefined_variables[arg1] = numbers[arg2]
            retval = arg1 + " = " + str(arg2)
        else:
            userdefined_variables[arg1] = arg2
            retval = arg1 + " = " + arg2

        print("119", arg1, arg2, to_ind)
        print("userdefined_variables", userdefined_variables)

        return retval, len(line), True

    if argname == "SWAP":
        arg1 = ""
        arg2 = ""
        ind += 1
        keyword = None
        if "with" in line:
            keyword = "with"
        elif "and" in line:
            keyword = "and"

        if keyword != None:
            split_ind = line.index(keyword)
            arg1 = "".join(line[ind:split_ind])
            arg2 = "".join(line[split_ind+1:])

        else:
            if invalid_args_following_func % 2 == 0:
                for i in range(ind + invalid_args_following_func // 2):
                    arg1 += line[i]

                for i in range(ind + (invalid_args_following_func)//2, ind + invalid_args_following_func):
                    arg2 += line[i]
            else:
                for i in range(ind + (invalid_args_following_func-1) // 2):
                    arg1 += line[i]

                for i in range(ind + (invalid_args_following_func-1) // 2, ind + invalid_args_following_func):
                    arg2 += line[i]
        # ind += 1
        # arg1 = line[ind]
        # ind += 2
        # arg2 = line[ind]
        retval = arg1 + " , " + arg2 +  " = " + arg2 + " , " + arg1
        return retval , len(line), False

    # if line[ind] == "initialize":
    #     ind += 1
    #     argline = line[ind:ind+invalid_args_following_func]
    #     # print("91", argline)
    #     keyword = "to"
    #     if "to" in argline:
    #         keyword = "to"
    #     elif "as" in argline:
    #         keyword = "as"
    #     to_ind = argline.index("to")
    #     arg1 = arg2 = ""
    #     if to_ind != -1:
    #         arg1 = "".join(argline[:to_ind])
    #         arg2 = "".join(argline[to_ind+1:])
    #     else:
    #         if invalid_args_following_func % 2 ==0:
    #             for i in range(ind + invalid_args_following_func // 2):
    #                 arg1 += line[i]
    #
    #             for i in range(ind + (invalid_args_following_func) // 2, ind + invalid_args_following_func):
    #                 arg2 += line[i]
    #         else:
    #             for i in range(ind + (invalid_args_following_func - 1) // 2):
    #                 arg1 += line[i]
    #
    #             for i in range(ind + (invalid_args_following_func - 1) // 2, ind + invalid_args_following_func):
    #                 arg2 += line[i]
    #
    #     # ind += 1
    #     # arg1 = line[ind]
    #     # ind += 2
    #     # arg2 = line[ind]
    #     retval = arg1 + " = " + arg2
    #     return retval, ind + invalid_args_following_func, True

    if argname == "INPUT":
        ind += 1

        retval = "".join(line[ind:])

        retval += " = input()"

        # retval = "input("
        # for i in range(ind+1, len(line)):
        #       retval += line[i] + " "
        # retval = retval[:-1]
        # retval += ")"
        return retval, len(line), False

    if argname == "ADD":
        retval = ""
        if "to" in line:
            to_ind = line.index("to")
#            add_ind = line.index("add")

            arg2 = "".join(line[ind+1:to_ind])
            arg1 = "".join(line[to_ind+1:])

            if arg2 in numbers:
                arg2 = numbers[arg2]

            retval = arg1 + " += " + arg2


        else:
            ind += 1
            arg1 = line[ind]
            ind += 2
            arg2 = line[ind]

            if arg2 in numbers:
                arg2 = numbers[arg2]

            retval = arg2 + " = " + arg1 + " + " + arg2
        return retval, len(line) , True

    # if line[ind] == "print":
    #     retval = "print(\" "
    #     ind += 1
    #     while ind < len(line):
    #         retval += line[ind] + " "
    #         ind += 1
    #     retval += " \")"
    #     return retval, ind+1, False

    if argname == "FUNCTION":
        
        curr_line = line[ind] + "("
        ind += 1
        args = []
        # print("162", num_args)
#        print(line)
        for _ in range(ind+1, len(line)):
            curr_line += line[ind]
            curr_line += ","
#            ind += 1
        if curr_line[-1] in ["is","end"]:
            curr_line = curr_line[:-1]
        
        curr_line += ")"
        # print("22", curr_line)

    return line[ind], ind+1, False

def group(line):
    # print("114", line)

    line = line.replace("is greater than or equal to", "\geq")
    line = line.replace("is less than or equal to", "\leq")
    # print("117", line)
    line = line.split(' ')
    line = [item.lower() for item in line if item != '']

    return line
    # USE NLP TO GROUP WORDS

def tokenize(filename):
    fp = open(filename, "r")
    
    program = []
    spaces = []
    for line in fp:
        lastchar = line[-1]
        line = line[:-1]
        num_spaces = 0
        for i in range(len(line)):
            if line[i] == ' ':
                num_spaces += 1
            else:
                break

        line = group(line)

        spaces.append(num_spaces)
        program.append(line)
        # print(line)
    # print("program is" , program)
    # if program[-1][-1] is not None:
    #     program[-1][-1] += lastchar
    return program, spaces


def translate(program,spaces):

    output = []
    # print(program)


    for i in range(len(program)):
        print(program[i])
        # validargs =[]
        # for j in range(len(program[i])):
        #     arg = program[i][j]
        #     if arg in table or arg in userdefined_functions or arg in userdefined_variables:
        #         validargs.append(True)
        #     else:
        #         validargs.append(False)

        curr_line = " "*spaces[i]

        j = 0
        seen_functional_item = False
        while j < len(program[i]):
            if program[i][j] in table:
                command = table[program[i][j]]
                seen_fuctional_item = True
            else:
                command = None
                # syn = syn_ant(program[i][j])
                # if syn is not None:
                #     for item in syn:
                #         if item in table:
                #             command = table[item]

                if command == None:
                    command = program[i][j]
            print(i,j, program[i][j], "is", command)
            if command == "func":
                temp_new_string, j, parse_again = createFunctionString(program[i], j)
                # print("new_string", new_string)
                new_string = ""
                for item in temp_new_string.split(" "):
                    if item in table and table[item] != "func":
                        new_string += table[item] + " "
                    else:
                        new_string += item + " "
                    # new_string += item + " "
                new_string = new_string[:-1]
                # if parse_again:
                #     new_string = translate([new_string.split(" ")] , [0])

                curr_line += new_string + " "
            else:
                curr_line += command + " "
                j += 1
            # print(i,j,command)

        # if not seen_fuctional_item:
        #     curr_line = useContextToTranslate(curr_line)

        output.append(curr_line)


    # print(output)
    return output

def findSpacing(output):
    spacing = []

    for line in output:
        curr_spacing = 0
        j = 0
        while j < len(line):
            if line[j] != " ":
                break
            else:
                curr_spacing += 1
                j += 1


        while curr_spacing % 4 != 0:
            curr_spacing += 1

        spacing.append(curr_spacing//4)

    return spacing

def containsConditional(line):
    tokens = line.split(" ")
    for token in tokens:
        if token in functions or token in userdefined_functions:
            return True
    else:
        return False

def findCorrectNumberTabsPerLine(output, tabsperline):
    goaltabsperline = []
    proper_tabs = [0,0]
    for i in range(len(tabsperline)):

        if tabsperline[i] > proper_tabs[-1]:
            tabsperline[i] = proper_tabs[-1]

        elif tabsperline[i] < proper_tabs[0]:
            tabsperline[i] = proper_tabs[0]

        elif tabsperline[i] not in proper_tabs:
            tabsperline[i] = proper_tabs[0]

        if containsConditional(output[i]):
            proper_tabs[0] = 0
            proper_tabs[1] = proper_tabs[1] + 1
        else:
            proper_tabs[0] = 0

    return tabsperline

def fixIndentation(output, tabsperline):
    goaltabsperline = findCorrectNumberTabsPerLine(output, tabsperline)

    result = [goaltabsperline[i]*" " + output[i][tabsperline[i]:] for i in range(len(output))]
    print(list(enumerate(goaltabsperline)))
    print(result)
    return result

    # print(list(enumerate(tabsperline)))
    #
    # for line in output:
    #     if containsFunction(line):
    #
