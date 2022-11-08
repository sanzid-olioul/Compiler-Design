import os
import sys
sys.path.append(os.path.join(os.getcwd(),'preprocessor'))
sys.path.append(os.path.join(os.getcwd(),'error'))
from preprocessor import RemoveComments
from preprocessor import Headers
from preprocessor import FunctionGrabber
BASE_PATH = os.getcwd()
SOURCE_FILE = 'Source.cpp'
FILE_PATH = os.path.join(BASE_PATH,SOURCE_FILE)
FUNCTION_CALLED = None
ERRORS = None
SOURCE_CODE = []
DEFINED_FUNCTIONS = None
with open(FILE_PATH) as sc:
    code = sc.readlines()
    for line in code:
        SOURCE_CODE.append(line)

rmc = RemoveComments(SOURCE_CODE)
SOURCE_CODE,SOURCE_LINE = rmc.get_code()
headers = Headers('\n'.join(SOURCE_CODE))
DEFINED_FUNCTIONS = headers()
if DEFINED_FUNCTIONS.get('main',None):
    main = DEFINED_FUNCTIONS['main']
    FUNCTION_CALLED,ERRORS = FunctionGrabber(SOURCE_CODE,SOURCE_LINE,'main',main['return_type']).check()
    if len(ERRORS)==0:
        ERRORS = None
    else:
        for error in ERRORS:
            try:
                raise error
            except Exception as e:
                print(e)

if not ERRORS:
    print('Build Successfullu..')


