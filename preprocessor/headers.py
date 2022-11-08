from header_library import HEADERS
from error import FileNotFound
import re
class Headers:
    def __init__(self,source_code):
        self.source_code = source_code
        self.functions = dict()
        self.headers = []
    def __call__(self):
        self._find_headers()
        self._find_functions()
        self.functions.update(self._grabber(self.source_code))
        return self.functions

    def _find_headers(self):
        headers = re.findall(r'#include[\s]*<([a-z.]+)>|#include[\s]*" *([a-z.]+)[\s]*"',self.source_code)
        headers = [x for sub in headers for x in sub if x!='']
        self.headers = headers

    def _find_functions(self):
        functions = dict()
        for header in self.headers:
            if HEADERS.get(header,None):
                functions.update(HEADERS[header])
            else:
                import os
                path = os.getcwd()
                # path = '/'.join(path.split(r'/')[:-1])
                full_path = os.path.join(path,header)
                try:
                    new_functions = self._function_grabber(full_path)
                    functions.update(new_functions)
                except FileNotFound as e:
                    t,m = e.args
                    print(t,'file',m)
        self.functions = functions
    def _grabber(self,txt):
        functions = re.findall(r'(int|float|double|char|void)[\s\*]+([A-Za-z][A-Za-z0-9_]*)\(([\s\w]*)\)',txt)
        dct = {fun : {
            'arg':{'raw':argu if argu else None},
            'return_type':rtn,
            'variables':[]
            } for rtn,fun,argu in functions}
        
        return dct
    def _function_grabber(self,path):
        txt = ''
        try:
            with open(path) as f:
                txt = f.read()
        except Exception:
            raise FileNotFound(path.split('/')[-1],'No such path found!')
        return self._grabber(txt)