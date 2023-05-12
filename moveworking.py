import json
from os import walk

in_path = 'Test/'
out_path = 'Test/output/'
write = 'working/'

def read_input(file):
    content = None
    with open(file, "r") as arq:
        content = json.load(arq)
    return content

files = next(walk(out_path), (None, None, []))[2]

for file in files:
    
    in_file_path = in_path+file
    out_file_path = out_path+file
    write_path = write+file
    
    in_content = read_input(in_file_path)
    out_content = read_input(out_file_path)
    
    if out_content['SolutionInfo']['ObjVal'] != 1e+100:
        with open(write_path, 'w') as arq:
            json.dump(in_content, arq)