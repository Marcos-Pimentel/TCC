import json
from os import walk

path = "tests_010_005/output/"

def read_input(file):
    content = None
    with open(file, "r") as arq:
        content = json.load(arq)
    return content

files = next(walk(path), (None, None, []))[2]

gap = 0
qtd = 0

for f in files:
    
    fpath = path+f

    content = read_input(fpath)

    sol = content['SolutionInfo']

    if sol['Status'] == 9 and sol['ObjVal'] != 1e+100:
        print('gap ' + str(f) + ': ' + str(sol['MIPGap']))
        gap += sol['MIPGap']
        qtd += 1
    
print(gap)
print(qtd)
print(gap/qtd)