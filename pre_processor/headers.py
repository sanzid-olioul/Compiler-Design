from header_library import HEADERS
import sys
import re
class Headers:
    def __init__(self,source_code):
        self.seouce_code = source_code
        self.functions = dict()
        self.headers = []
    def __call__(self):
        self._find_headers()
        self._find_functions()
        return self.functions

    def _find_headers(self):
        headers = re.findall(r'#include[\s]*<([a-z.]+)>|#include[\s]*" *([a-z.]+)[\s]*"',self.seouce_code)
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
                new_functions = self._function_grabber(full_path)
                functions.update(new_functions)
        self.functions = functions

    def _function_grabber(self,path):
        txt = ''
        with open(path) as f:
            txt = f.read()
        functions = re.findall(r'(?:int|float|double|char|void)[\s]*([A-Za-z][A-Za-z0-9_]*)\([\s]*\w*\)',txt)
        dct = {fun : {'arg':{}} for fun in functions}
        return dct