import re
import os
import sys
sys.path.insert(1,os.path.join(os.getcwd(),'pre_processor'))
print(os.path.join(os.getcwd(),'pre_processor'))
from pre_processor.comments import DeleteComments
from pre_processor.headers import Headers

#File path related stuff
BASE_DIR = os.getcwd()
FILE_NAME = 'source.cpp'
FilePath = os.path.join(BASE_DIR,FILE_NAME)

#Basic C leywords
PREPROCESSORS = ('define','include','undef','ifdef','ifndef','if','else','elif','endif','error','pragma')
BASIC_HEADERS = ('stdio.h','conio.h','math.h','string.h')
DATATYPES_MODIFIERS ={
    'short':('int'),
    'long':('int','double'),
    'unsigned': ('int'),
    'const':('int','char','double','float'),
}
DATATYPES = ('int','char','double','float','void')


def is_preprocessor(line):
    '''
    Checking whether it is a valid preprocessor or not!
    '''
    if line[0] != '#':
        return False
    else:
        res = re.findall(r'[a-z.]+',line)
        if res[0] in PREPROCESSORS:
            if res[0] == PREPROCESSORS[1]:
                temp = re.findall(r'<[a-z.]+>',line)
                custom = re.findall(r'"[a-z.]+"',line)
                if len(temp)==1:
                    temp = temp[0][1:-1]
                    if temp in BASIC_HEADERS:
                        return True
                    else:
                        raise Exception('Not a valid header!')
                elif len(custom)==1:
                    custom=custom[0][1:-1]
                    header_path = os.path.join(BASE_DIR,custom)
                    if os.path.exists(header_path):
                        pass
                    else:
                        raise Exception('No such header exists!')
                else:
                    raise Exception('Syntax err , Please check',line)




# def find_main():
#     if 'main' in line:
#         # match = re.findall(r'int[/s]+main[/s]+([/s]+)[/s/n]*{[a-zA-Z0-9]*}')

#File opening for check

with open(FilePath,'r') as f:
    txt = f.read()
    code = DeleteComments(txt)
    head = Headers(txt)
    head = head()
    # code = code()
    print(head)


# with open(FilePath,'r') as f:
#     linr_number = 1
#     for line in f:
#         line = line.strip()
#         tags = line.split(' ')
#         is_preprocessor(line)
#         print(linr_number,tags)
#         linr_number+=1
