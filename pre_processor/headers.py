from header_library import HEADERS
import re
class Headers:
    def __init__(self,source_code):
        self.seouce_code = source_code
        self.functions = dict()
        self.headers = []
    def __call__(self):
        self._find_headers()
        
    def _find_headers(self):
        headers = re.findall(r'#include[\s]*<([a-z.]+)>|#include[\s]*" *([a-z.]+)[\s]*"',self.seouce_code)
        headers = [x for sub in headers for x in sub if x!='']
        self.headers = headers

    def _find_functions(self):
        pass