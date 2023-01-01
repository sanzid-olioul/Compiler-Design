import re
class VariableDeclearation:
    def __init__(self):
        self._initialize = r"^(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-0_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*|[0-9]*|'[a-zA-z0-9]')\s*;"
        self._declear = r"^(int|void|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*\s*(?:\s*;|(?:\s*,\s*(?:[a-zA-Z_][a-zA-Z0-9_]*))*));"
        self._update = r"(^[a-zA-Z_][a-zA-Z0-0_]*)\s*=\s*(.+)\s*;"
    
    def initialized(self,line):
        return re.findall(self._initialize,line)
    
    def decleard(self,line):
        res = re.findall(self._declear,line)
        if res:
            temp = res[0][1].split(',')
            return (res[0][0],[t.strip() for t in temp])

        return None 

    def update(self,line):
        res = re.findall(self._update,line)
        if res:
            return res[0][0],res[0][1]
